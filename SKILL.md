---
name: bilingual-html-documents
description: Use when turning plans, notes, or supplied articles into bilingual Chinese/English standalone HTML.
version: 1.0.0
author: Benny (benny2744), Hermes Agent
license: MIT
platforms: [linux, macos, windows]
triggers:
  - turn a lesson plan into a student-facing HTML guide
  - turn meeting notes into a bilingual colleague HTML brief
  - preserve an article's exact English wording in a bilingual HTML edition
  - generate standalone Chinese English documents
metadata:
  hermes:
    tags: [html, bilingual, lessons, meetings, standalone]
---

# Bilingual HTML Documents

Generate audience-adapted Chinese/English documents in a warm editorial style. This is a local document workflow, not an LMS, translation service, or publication tool. An agent or human supplies both language versions; the Python renderer performs deterministic validation and rendering without network access.

## Stable Default

Version 1.0 uses a fluid laptop-width layout, unified fixed desktop command panel, one Chinese/English switch, inline SVG icon actions with translated hover/focus tips, framed contents links and collapsible sections. Mobile uses an above-document panel. Preserve these defaults unless the user requests a change; examples are fictional fixtures, not content to reuse in real documents.

This repository is a standalone skill with its supporting renderer, schema, examples, references, and tests. Static deployment packaging is supported. Integration with a particular hosting platform still requires its documented contract and separate authorization; do not claim a platform adapter is included.

## When to Use

- Turn a lesson plan into a student guide, meeting notes into a colleague brief, or a supplied article into a full bilingual reading edition.
- Produce a portable single HTML with a language switcher and Download HTML control.
- Do not use for authoring new curriculum, retrieving meetings, sending messages, or automatically deploying sites.

## Contract

- Every reader-facing string is paired in `zh` and `en`; code/names/URLs may be identical.
- Article mode preserves supplied source wording in the source language and translates it, rather than summarizing or rewriting it.
- Standalone HTML opens offline, includes inline CSS/JS/SVG, and does not depend on CDNs or external fonts.
- Student content excludes teacher-only directions and personal information; meeting content preserves agreed versus tentative status.
- Leadership-facing briefs are standalone documents: include the subject, substantive assessment and necessary date/evaluator metadata, but omit recipient-role preambles, assistant/process commentary, private source provenance and speaker-only instructions. Use full Chinese/English content, not paired headings over an English-only body. For authorized personnel reviews, retain the supervisor's relevant judgments, preserve their rating strength and distinguish proposed follow-up from agreed commitments.
- Hidden language content is not a privacy boundary. Omitted material must be absent from HTML, comments, and embedded data.
- Sources stay unchanged; private review notes stay out of shareable packages; live publication requires explicit approval.

## Prerequisites

- Python 3.10+ standard library for rendering and unit tests.
- Source access authorized for the intended audience.
- Browser for runtime verification; local-only generation requires no design or hosting service.
- Read `references/content-modes.md`, `references/design-system.md`, and `references/deployment.md` when applicable. For article mode, also read `references/article-mode.md`.

## Phases / Procedure

1. **Establish source and audience.** Read exact source files with the available file tools; choose lesson, meeting, or article mode, and student/internal/public visibility. Latest meeting means meeting date, not modification timestamp. Record source paths/section evidence privately. Public sharing requires a separate boundary check.
2. **Choose the right transformation.** Lesson and meeting modes adapt content according to their source-backed rules. For article mode, follow `references/article-mode.md`: preserve exact supplied source-language wording and translate it; never summarize or silently edit the source text. Missing deadlines/owners remain unconfirmed. Surface contradictions visibly. Editorial additions must be labeled as such.
3. **Prepare structured content.** Use `templates/document.schema.json` and fictional examples in `assets/examples/`. Pair every label and block in Chinese/English, including metadata, table cells and links. Keep source/private paths out of document JSON; preserve numbers, names, date precision, modal strength, and URLs.
4. **Review privacy and semantics.** Check both language versions. Exclude teacher dashboards, private attachments, student names/images, staff judgments and partner/student case details not needed by recipients. Document omissions and uncertainty in a private report, never inside the deployment ZIP. Credentials in source are a blocker.
5. **Render.** Invoke `scripts/render.py` in a shell, using explicit input/output paths. It validates before writing, refuses overwrites, and creates a static deployment ZIP only when requested. The schema content is data, never executable HTML.
6. **Verify.** Run unit tests, then open fictional and real outputs in a browser. Test both languages, mobile overflow, no-JS fallback, offline dependencies, print CSS and actual Download HTML/reopening. Scan generated HTML for private/source-only strings. Automated translation-pair completeness is not a semantic or confidentiality guarantee.
7. **Deliver.** State absolute paths to individual HTMLs and optional static ZIPs, source titles, checks passed, and unresolved review items. Do not upload, publish, assign homework, or send messages without approval.

## How to Run

From the skill directory (or use absolute script paths):

```text
python3 scripts/render.py --input /path/to/document.json --output /path/to/document.html --package /path/to/document-deploy.zip
python3 scripts/validate.py /path/to/document.json
python3 scripts/test_documents.py
```

The generated browser files themselves require no Python or build process.

## Output Format

- One `.html` per document, complete in both languages with the language switcher, Download HTML and Print at the top of a unified floating command/contents panel; use a fluid laptop-width reading layout.
- Initially expanded, individually collapsible sections; fixed desktop command panel with one Chinese/English switch and five inline-SVG icon actions (download, print, expand all, collapse all, back to top). Translate accessible names and hover/focus tooltips with the selected language; give contents links individually bordered rounded frames. Use 44px icon hit targets. Mobile navigation sits above the document. Print includes every section, and download retains the full document.
- Optional per-document static ZIP with `index.html` and safe deployment README; no source JSON or private reports.
- Local review report outside the shareable package when adapting real sources.
- Save generated files to the user-requested output location or a clearly named local artifact directory. Keep confidential personnel reviews and private review materials out of ordinary delivery batches.

## Anti-Patterns / Pitfalls

- Do not copy prototype Tailwind/Google Fonts/Material Symbols dependencies.
- Do not treat teacher notes as learner instructions or tentative suggestions as agreed policy.
- Do not summarize, paraphrase, normalize, or silently correct article text in exact-wording mode; keep translator notes separate and explicitly labeled.
- Do not simplify bilingual by showing bilingual headings while leaving tables/controls untranslated.
- Do not embed raw source text in hidden DOM, JSON, comments, or downloaded files.
- Do not promise private hosting from an unlisted URL: standalone files have no access controls.
- Do not infer dates from weekdays when source dates conflict; flag confirmation instead.
- Compare meeting summaries with the underlying dialogue before assigning policy strength or scoring responsibility: compressed summaries can turn preferences into mandates or teacher grading into student self-grading.
- Preserve mandatory conditions in both languages (for example AI attribution and individual on-camera participation), not only the prominent durations or deadlines.
- For automated download verification, capture the actual Blob generated by the click handler, save it and reopen it; report this separately from native browser save-dialog verification.
- Check computed visibility of `.js-only` controls with JavaScript disabled; later component display rules can override a basic class selector. Preserve the final `html:not(.has-js) .js-only` hiding rule and test the actual fallback, not just the presence of `<noscript>`.
- Do not generate PDFs unless requested; Print uses browser print only.

## Verification

- Unit suite verifies validation, escaping, allowed URLs, output refusal and ZIP allowlist.
- Browser verifies top control, `html.lang`, page title, visible controls, no-JS fallback, storage failures, download reopening, mobile layout and network independence.
- Human semantic review verifies translation equivalence, policy strength, source fidelity and audience-safe omissions.
- Article mode additionally compares the rendered source-language text against the supplied article, including title, deck, headings, captions and closing copy.

## Tools Used

Use available file reading/searching/writing tools for sources and structured inputs, a shell for deterministic rendering/tests, and browser automation or visual inspection for verification when available. No specific agent platform or network service is required. Optional design references are read-only and must never receive sensitive source material.
