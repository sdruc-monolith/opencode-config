#!/bin/sh
set -eu

DATA_DIR=${OPENCODE_DATA_DIR:-$HOME/.local/share/opencode}
MAIN_DB=${OPENCODE_DB:-$DATA_DIR/opencode.db}
LOCAL_DB=${OPENCODE_LOCAL_DB:-$DATA_DIR/opencode-local.db}
DAYS=30
BATCH_SIZE=10
EXECUTE=0
LIST_CANDIDATES=0
KEEP_PREDICATE=''
KEEP_PARENT_PREDICATE=''

usage() {
  printf '%s\n' \
    'Usage: delete-old-opencode-sessions.sh [--days N] [--batch-size N] [--list] [--keep-session ID] [--execute]' \
    '' \
    'Defaults to a dry run for sessions not updated in the last 30 days.' \
    '--list prints the exact candidate sessions.' \
    '--keep-session can be repeated to protect specific session IDs.' \
    'Use --execute to permanently delete matching sessions and compact both databases.'
}

die() {
  printf '%s\n' "delete-old-opencode-sessions: $*" >&2
  exit 1
}

has_table() {
  [ "$(sqlite3 "$1" "SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='$2';")" = 1 ]
}

old_session_count() {
  sqlite3 -noheader "$1" "SELECT COUNT(*) FROM session WHERE time_updated < $CUTOFF_SQL $KEEP_PREDICATE;"
}

new_child_count() {
  sqlite3 -noheader "$1" \
    "SELECT COUNT(*) FROM session child JOIN session parent ON child.parent_id = parent.id WHERE parent.time_updated < $CUTOFF_SQL $KEEP_PARENT_PREDICATE AND child.time_updated >= $CUTOFF_SQL;"
}

list_candidates() {
  sqlite3 -header -column "$1" \
    "SELECT id, datetime(time_updated / 1000, 'unixepoch', 'localtime') AS updated, title, directory FROM session WHERE time_updated < $CUTOFF_SQL $KEEP_PREDICATE ORDER BY time_updated;"
}

ensure_closed() {
  if lsof -nP "$1" "$1-wal" "$1-shm" 2>/dev/null; then
    die "OpenCode still has $1 open; close all OpenCode sessions and rerun"
  fi
}

check_foreign_keys() {
  violations=$(sqlite3 "$1" 'PRAGMA foreign_key_check;') || die "could not check $1"
  [ -z "$violations" ] || die "foreign-key violations found in $1"
}

validate_database() {
  quick_check=$(sqlite3 "$1" 'PRAGMA quick_check;') || return 1
  [ "$quick_check" = "ok" ] || return 1

  foreign_key_check=$(sqlite3 "$1" 'PRAGMA foreign_key_check;') || return 1
  [ -z "$foreign_key_check" ]
}

cleanup_compaction() {
  rm -f "$compact_path"
  if [ "${restore_needed:-0}" -eq 1 ] && [ ! -e "$db" ] && [ -e "$backup_path" ]; then
    mv "$backup_path" "$db"
  fi
}

compact_database() {
  db=$1
  compact_path="${db}.compact"
  backup_path="${db}.before-compaction.$$"
  restore_needed=0

  ensure_closed "$db"
  trap cleanup_compaction EXIT HUP INT TERM
  rm -f "$compact_path"

  sqlite3 "$db" "PRAGMA wal_checkpoint(TRUNCATE); VACUUM INTO '$compact_path';"
  validate_database "$compact_path" || die "compacted database failed validation: $db"

  mv "$db" "$backup_path"
  restore_needed=1
  rm -f "$db-wal" "$db-shm"
  mv "$compact_path" "$db"

  if ! validate_database "$db"; then
    rm -f "$db"
    mv "$backup_path" "$db"
    restore_needed=0
    die "swapped database failed validation; original restored: $db"
  fi

  rm -f "$backup_path"
  restore_needed=0
  trap - EXIT HUP INT TERM
  printf 'Compaction complete: %s\n' "$db"
  df -h "$(dirname "$db")"
}

delete_batches() {
  db=$1
  label=$2
  delete_events=$3
  event_delete=''

  if [ "$delete_events" -eq 1 ]; then
    event_delete='DELETE FROM event_sequence WHERE aggregate_id IN (SELECT id FROM cleanup_session_ids);'
  fi

  initial_count=$(old_session_count "$db")
  printf '%s: %s sessions older than %s days\n' "$label" "$initial_count" "$DAYS"

  if [ "$LIST_CANDIDATES" -eq 1 ]; then
    list_candidates "$db"
  fi

  if [ "$EXECUTE" -eq 0 ] || [ "$initial_count" -eq 0 ]; then
    return 0
  fi

  ensure_closed "$db"

  while [ "$(old_session_count "$db")" -gt 0 ]; do
    sqlite3 "$db" "
      PRAGMA busy_timeout=30000;
      PRAGMA foreign_keys=ON;
      BEGIN IMMEDIATE;
      CREATE TEMP TABLE cleanup_session_ids (id TEXT PRIMARY KEY);
      INSERT INTO cleanup_session_ids
        SELECT id FROM session
        WHERE time_updated < $CUTOFF_SQL $KEEP_PREDICATE
        ORDER BY time_updated
        LIMIT $BATCH_SIZE;
      $event_delete
      DELETE FROM session WHERE id IN (SELECT id FROM cleanup_session_ids);
      COMMIT;
      PRAGMA wal_checkpoint(TRUNCATE);
    " >/dev/null
  done

  remaining=$(old_session_count "$db")
  [ "$remaining" -eq 0 ] || die "$label cleanup did not finish"
  check_foreign_keys "$db"
  printf '%s: cleanup complete\n' "$label"
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    --days)
      [ "$#" -ge 2 ] || die '--days requires a number'
      DAYS=$2
      shift 2
      ;;
    --days=*)
      DAYS=${1#*=}
      shift
      ;;
    --batch-size)
      [ "$#" -ge 2 ] || die '--batch-size requires a number'
      BATCH_SIZE=$2
      shift 2
      ;;
    --batch-size=*)
      BATCH_SIZE=${1#*=}
      shift
      ;;
    --execute)
      EXECUTE=1
      shift
      ;;
    --list)
      LIST_CANDIDATES=1
      shift
      ;;
    --keep-session)
      [ "$#" -ge 2 ] || die '--keep-session requires a session ID'
      keep_id=$2
      shift 2
      ;;
    --keep-session=*)
      keep_id=${1#*=}
      shift
      ;;
    --help|-h)
      usage
      exit 0
      ;;
    *)
      usage >&2
      die "unknown option: $1"
      ;;
  esac

  if [ "${keep_id+x}" = x ]; then
    case "$keep_id" in
      ses_[A-Za-z0-9]*) ;;
      *) die "invalid session ID: $keep_id" ;;
    esac
    KEEP_PREDICATE="$KEEP_PREDICATE AND id <> '$keep_id'"
    KEEP_PARENT_PREDICATE="$KEEP_PARENT_PREDICATE AND parent.id <> '$keep_id'"
    unset keep_id
  fi
done

case "$DAYS" in
  ''|*[!0-9]*) die '--days must be a positive integer' ;;
esac
case "$BATCH_SIZE" in
  ''|*[!0-9]*) die '--batch-size must be a positive integer' ;;
esac
[ "$DAYS" -gt 0 ] || die '--days must be greater than zero'
[ "$BATCH_SIZE" -gt 0 ] || die '--batch-size must be greater than zero'

command -v lsof >/dev/null 2>&1 || die 'lsof is required'
command -v sqlite3 >/dev/null 2>&1 || die 'sqlite3 is required'

if [ "$EXECUTE" -eq 1 ]; then
  [ -f "$MAIN_DB" ] && ensure_closed "$MAIN_DB"
  [ -f "$LOCAL_DB" ] && ensure_closed "$LOCAL_DB"
fi

CUTOFF_SQL="strftime('%s','now','-${DAYS} days') * 1000"

for db in "$MAIN_DB" "$LOCAL_DB"; do
  [ -f "$db" ] || continue
  has_table "$db" session || continue

  children=$(new_child_count "$db")
  [ "$children" -eq 0 ] || die "$db has old sessions with newer child sessions"
done

if [ "$EXECUTE" -eq 0 ]; then
  printf 'Dry run only. Pass --execute to delete sessions.\n'
fi

if [ -f "$MAIN_DB" ] && has_table "$MAIN_DB" session; then
  delete_batches "$MAIN_DB" 'main database' 1
fi

if [ -f "$LOCAL_DB" ] && has_table "$LOCAL_DB" session; then
  delete_batches "$LOCAL_DB" 'local database' 0
fi

if [ "$EXECUTE" -eq 1 ]; then
  if [ -f "$MAIN_DB" ]; then
    compact_database "$MAIN_DB"
  fi
  if [ -f "$LOCAL_DB" ] && [ "$LOCAL_DB" != "$MAIN_DB" ]; then
    compact_database "$LOCAL_DB"
  fi
fi
