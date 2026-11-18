# Bilingual article sharing mode

Use `kind: "article"` when the user wants a complete bilingual edition of a supplied article, rather than a summary or adapted guide.

## Preserve the source

- Keep every source-language passage exactly as supplied: spelling, punctuation, capitalization, dates, figures, names, paragraph wording and even apparent errors. Do not silently fix, shorten, reorder, or paraphrase it.
- Translate each passage into the requested second language. Translation may be idiomatic, but must preserve meaning, uncertainty, attribution, emphasis and tone; it must not introduce additional claims.
- Include supplied headline, deck/subtitle, section headings, chart labels, image captions, footnotes, end marks and calls to action when present. Do not invent missing bylines, image descriptions, links, or publication metadata.
- If the source includes non-prose such as a chart, preserve its caption and labels as text only when supplied; do not fabricate chart values or visual assets.
- If exact matching is impossible because the input is incomplete or corrupted, pause or mark the omission in a separately labeled editorial note. Never disguise an omission as source text.

## Structure the HTML

- Set `kind` to `article`; retain the normal bilingual document schema and standalone renderer.
- Use metadata for publication, date and stated reading time only when provided. Keep source title and deck in the document title/subtitle.
- Divide the article into sections matching its original heading hierarchy. Within each section, use one paragraph block per source paragraph, with the source wording and translation paired in the same block. Preserve paragraph order.
- Use lists, tables, or callouts only when the source itself contains those structures. Do not add a summary, analysis, discussion questions, glossary or learning activity unless requested; if requested, place clearly labeled editorial material outside the article text.
- The bilingual notice must accurately say whether the source language is verbatim and identify the translated language; do not claim an official translation.

## Verification

- Compare the rendered source-language article text with the provided input, preferably mechanically where feasible; confirm all front/back matter and captions are included and ordered correctly.
- Review both language versions for translation fidelity, particularly numbers, names, units, dates, negation, modal strength, quotations and attributions.
- Open the actual HTML in a browser and test the language switch, section navigation, download, print and offline behavior as required by the parent skill.
- Do not publish, upload, send or share externally unless the user separately authorizes that action.
