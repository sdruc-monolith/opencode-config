---
name: ui-app-testing
description: UI application development, debugging, visual and layout review, and testing with Docker, Docker Compose, local Kubernetes, and Playwright. Use when changing or diagnosing a web UI, frontend, full-stack app, browser workflow, responsive layout, visual design, styling, or user interaction.
---

# UI Application Workflow

Treat a UI change as incomplete until the application has been run and the affected behavior has been exercised in a real browser. Static inspection, type checking, unit tests, and successful builds are useful but do not replace browser validation.

## Default Behavior

- Inspect the repository before editing. Find its README, development scripts, package manager, Dockerfiles, Compose files, Kubernetes manifests, Helm charts, Makefile or task runner, environment examples, health endpoints, and existing end-to-end tests.
- Reuse the application's documented local workflow and existing infrastructure. Do not invent a parallel deployment path merely because it is familiar.
- Start the dependencies needed to exercise the changed behavior. Prefer Docker Compose or the repository's documented container command for ordinary local stacks. Use local Kubernetes when Kubernetes behavior, ingress, service discovery, operators, charts, or manifests are part of the change or when it is the project's established development path.
- Use the available Playwright browser tools against the running application. Do not stop after reporting that the code compiles or that unit tests pass.
- Inspect the rendered UI visually at relevant viewport sizes. Correct functionality with broken spacing, hierarchy, alignment, overflow, or responsive behavior is not complete.
- Work autonomously through startup and browser validation when the required tooling and configuration are available. Do not ask the user to perform routine local deployment or browser checks on the agent's behalf.
- Never claim that a UI was verified unless it was loaded and exercised in a browser during the current task.

## Workflow

### 1. Discover the Supported Run Path

Before changing code:

1. Identify the frontend entry point and any backend, database, authentication, queue, object storage, or API dependencies needed by the affected flow.
2. Locate the canonical commands in project documentation and automation rather than guessing commands from filenames alone.
3. Check whether services are already running before starting duplicates or taking over ports.
4. Identify required environment variables and use repository-provided development defaults or example files. Never print, commit, or invent secrets.
5. Find existing browser tests, fixtures, seeded users, mock modes, and test-data setup that can make the flow deterministic.

### 2. Make the Smallest Correct Change

- Preserve the existing design system, component patterns, routing, state management, API contracts, and responsive conventions.
- Address loading, empty, success, error, disabled, and permission states that are directly affected by the change.
- Keep accessibility semantics intact: labels, roles, keyboard operation, focus behavior, and meaningful status or error announcements.
- Avoid broad visual redesigns or new dependencies unless the task requires them.
- Add or update automated tests at the appropriate level, but retain browser validation as the final integration check.

### 3. Start a Representative Local Environment

Use the lowest-cost environment that faithfully exercises the behavior:

1. Use the repository's native dev server when it includes or mocks all relevant boundaries.
2. Use Docker or Docker Compose when multiple services or container behavior are needed.
3. Use local Kubernetes when cluster-specific behavior matters or the repository expects it. Reuse an existing local context when safe; otherwise use the project's documented kind, minikube, k3d, Tilt, Skaffold, DevSpace, Helm, or equivalent workflow.

For containerized or Kubernetes deployments:

- Build the changed image rather than accidentally testing a stale tag or cached artifact.
- Verify the active Docker/Kubernetes context before creating or changing resources. Never deploy a development build to a remote or shared cluster as a substitute for local testing.
- Use isolated project names, namespaces, releases, ports, or labels when the tooling supports them.
- Wait for health checks, rollout completion, and application readiness. A running container or pod is not sufficient evidence that the app is usable.
- Inspect service logs and events when startup fails. Fix failures caused by the change or local configuration instead of abandoning browser testing at the first error.
- Use port forwarding or the documented local ingress route, and record the exact URL being tested.

### 4. Validate with Playwright

Use Playwright against the running URL and test the user-visible outcome, not only page load:

1. Navigate to the affected route and wait for the application to reach a stable ready state.
2. Exercise the primary changed workflow using user-facing roles, labels, and text where possible.
3. Assert or inspect the resulting visible state, navigation, persisted data, and relevant API outcome.
4. Exercise a meaningful failure or edge state when the change affects validation, errors, permissions, empty data, or loading.
5. Check browser console errors and failed network requests. Investigate new errors even when the page appears correct.
6. Test at a desktop viewport and a representative mobile viewport for layout-affecting changes.
7. Capture screenshots when visual comparison, clipping, overlap, responsive behavior, or final evidence is useful. Prefer accessibility snapshots for locating and operating controls.
8. Reload or revisit the flow when persistence, routing, hydration, or state restoration is relevant.

Do not treat DOM injection, direct JavaScript state mutation, or calling application internals as a substitute for the user workflow. Such techniques are acceptable only for targeted diagnosis after the real interaction has exposed a problem.

### 5. Review Visuals and Layout

Visual validation is required for changes that render or affect UI. Use Playwright screenshots and viewport resizing to inspect the actual page, not just its DOM or accessibility tree.

- Test the project's supported breakpoints. At minimum, inspect one representative desktop viewport and one representative mobile viewport for layout-affecting work; add tablet or intermediate widths when wrapping or breakpoint transitions may fail.
- Inspect the whole relevant page and focused screenshots of changed components. Scroll through content that extends below the fold.
- Check alignment, spacing rhythm, grouping, visual hierarchy, typography, icon sizing, borders, radii, shadows, and consistency with surrounding components and the existing design system.
- Check for horizontal scrolling, clipped text, unintended wrapping, overlapping layers, off-screen controls, collapsed containers, excessive empty space, content jumping, and fixed or sticky elements obscuring content.
- Exercise long labels, realistic content, empty states, validation messages, loading indicators, and error states when they can change geometry.
- Inspect interactive states that matter to the change: hover, focus-visible, pressed, selected, disabled, expanded menus, dialogs, popovers, tooltips, and toasts. Verify overlays have correct positioning, stacking, dismissal, and scroll behavior.
- Verify images and media preserve appropriate aspect ratios and do not stretch, crop unexpectedly, or cause layout shifts.
- Check readable contrast and visible focus treatment. Use existing automated accessibility checks when available, but do not treat them as a substitute for visual inspection.
- Compare against supplied designs, screenshots, stories, or established neighboring pages when available. Do not invent a new visual language for an existing application.
- If the repository has visual regression tests, update baselines only after inspecting the diff and confirming the new rendering is intentional. Never accept changed snapshots merely to make tests pass.

When a visual defect is found, fix it and repeat the relevant screenshots and interactions. Do not report a known clipping, overlap, or responsive defect as acceptable unless it is explicitly outside the requested scope.

### 6. Verify and Clean Up

- Run the repository's relevant formatter, linter, type checker, unit or integration tests, build, and existing end-to-end tests.
- Keep the local environment running while diagnosing failures so logs, network traffic, and browser state remain available.
- Remove only resources created for the task. Do not tear down pre-existing containers, namespaces, clusters, volumes, or user processes.
- Preserve useful screenshots or traces only when the repository has an established artifact location or they are needed to explain a failure.

## When Full Local Deployment Is Blocked

Attempt reasonable recovery before falling back: inspect logs, resolve port conflicts without killing unrelated processes, install dependencies through the project's package manager, build missing images, wait for rollouts, and use documented mock or seed modes.

If deployment or browser validation is genuinely impossible because of unavailable credentials, inaccessible external systems, unsupported host architecture, missing licensed software, or a broken dependency outside the task's scope:

- State the exact command or stage that failed and the relevant error.
- Complete the strongest available static, unit, integration, and build checks.
- Clearly label browser verification as not performed; do not imply the UI works.
- Give the smallest concrete step needed to unblock the browser check.

## Completion Report

Summarize:

- The implementation and user-visible behavior changed.
- How the app was run, including Docker/Compose/local Kubernetes when used.
- The URL and Playwright workflows exercised, including viewports and edge states when relevant.
- The visual and responsive layouts inspected and any screenshots or visual-regression checks used.
- Automated checks run and their outcomes.
- Any remaining blocker or unverified behavior.
