---
description: Find recent alphaXiv papers that match Zotero research interests, import good fits, and add blog-style notes
---

You are scouting recent research papers for my Zotero library. Optional user guidance, constraints, or limit is provided in the `user_prompt` tag:

<user_prompt>
$ARGUMENTS
</user_prompt>

Use the current date as the reference date.

Goal:
Find recent alphaXiv/arXiv papers that fit my research interests. Add only strong matches to Zotero, write a concise blog-style note for each import, and create a short dated run report directly in the top-level `Research Interests` collection.

Research-interest source of truth:
- Use Zotero first. Look for the top-level collection named `Research Interests`, then read the item titled `Research Interests Summary` and its child note(s).
- If that item is unavailable, infer interests from the Zotero collection tree, especially: Physical AI, Agentic Scientific Discovery, SciML, Data Center, LLM, Battery, Semiconductor, and Anomaly Detection.
- Let these research interests dictate prioritization. Treat the `user_prompt` contents as optional constraints or hints, not as the primary ranking signal unless the user explicitly says to focus exclusively on something.

Collection semantics:
- Treat the top-level `Research Interests` collection as an organizational/reporting collection, not the default destination for imported papers.
- Put run reports and research-interest summary material directly in `Research Interests`.
- Put imported papers in the most relevant existing topic subcollection or other specific collection.
- Do not also add imported papers directly to `Research Interests` unless no better topic or specific collection exists. If this fallback is used, mention it in the run report.

Discovery workflow:
1. Search alphaXiv/arXiv for recent papers related to my interests. Default to the last 30 days and at most 5 imports unless the `user_prompt` contents say otherwise.
2. Prioritize from the Research Interests summary and Zotero collection structure. Treat the `user_prompt` contents as constraints or focus guidance.
3. Include a small amount of adjacent/trending exploration when it plausibly connects to my interests.
4. Avoid duplicates by checking title, arXiv ID, DOI, or URL before importing.
5. Import only strong fits. If nothing is strong enough, add nothing and report why.

Zotero filing rules:
- Add each imported paper using its arXiv URL or DOI, with PDF attachment when available.
- Perform Zotero write operations sequentially, not in parallel. Finish one import, collection assignment, and note creation before starting the next paper.
- If an import with `attach_mode: auto` times out, retry that paper once with `attach_mode: none`, then continue with notes/reporting and mention that the PDF attachment was skipped.
- File it into the best existing topic or specific collection by comparing the paper's actual contribution against the current Zotero collection names and nearby items. Prefer the most specific good fit, but use a broader topic collection when the match is cross-cutting or uncertain.
- Do not ask interactive questions. If no ideal collection exists, file the paper into the closest existing collection and report the compromise. Only create a new collection when the user explicitly requests it in the `user_prompt` contents.
- Add useful tags such as `research-scout`, `alphaxiv`, and short topic tags inferred from the paper and chosen collection. For exploratory/trending additions, also add `adjacent-interest` or `trending` as appropriate.

Blog-post note requirements:
For each newly imported paper, create a child Zotero note titled `Blog Post - <paper title>`. Write a substantive technical blog-style analysis note, not a brief abstract recap and not a placeholder draft. Aim for enough detail that I could later turn it into a public post without rereading the paper from scratch. Include these sections:
- Title
- One-sentence hook
- Why this paper fits my research interests: connect the paper to specific interests, collections, or recurring themes in my Zotero library.
- Problem and context: explain what problem the paper is addressing and why it matters.
- Main idea: describe the core method or insight in plain technical language.
- Key technical contributions: list the concrete contributions, mechanisms, datasets, experiments, or theoretical results that make the work notable.
- Results and evidence: summarize the strongest evidence from the abstract, metadata, or paper content, and avoid claims not supported by the source.
- Limitations or caveats: note what the paper does not establish, what assumptions it makes, or what remains unclear.
- What I would look at next: include specific follow-up questions, experiments, comparisons, or adjacent papers to investigate.
- Suggested Zotero collection and tags
Prefer several short paragraphs plus bullets where useful. Do not keep the note tiny unless the available paper information is genuinely sparse; if source detail is sparse, say that and explain what would need to be checked in the full paper.

Run report requirements:
- Create one separate Zotero document item in the `Research Interests` collection for every run, even if no papers are imported. Do not attach the run report as a child note to `Research Interests Summary`.
- If the `user_prompt` contents contain a meaningful focus, name the report `Research Scout - <Concise Focus> - YYYY-MM-DD`; otherwise use `Research Scout Report - YYYY-MM-DD`. Append a short time if needed to avoid duplicate titles.
- Put a concise status report in the item's abstract/summary field when creating the item.
- Always create a child note on the report item titled `Paper Summary - <report title>`.
- In the child summary note, briefly cover search scope, priorities used, papers added, notable duplicates or rejected candidates, collection choices, and useful follow-up questions.
- Keep the child summary note concise but useful. Prefer specific claims from paper metadata, abstracts, or content over generic praise.
- Tag the report item with `research-scout-report` and `alphaxiv`. Tag the child summary note with `research-scout-summary` and `alphaxiv`.

Important constraints:
- Do not fabricate claims. Use alphaXiv/arXiv metadata, abstracts, and paper content where available.
- Do not add weak matches just to fill a quota.
- Prefer fewer high-quality additions over many marginal ones.
- Do not stop to ask for clarification during headless runs; make the safest conservative decision, document it, and continue.
- At the end, report papers added, Zotero item keys, exact collection names used, blog note keys, run report item key, run report summary note key, and candidates rejected with brief reasons.
