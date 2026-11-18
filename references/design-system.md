# Warm editorial document design

The design direction is a warm editorial curriculum/document interface: spacious reading cards, serif headings, subtle warm borders, and a compact command panel. The renderer implements the design independently with embedded CSS, JavaScript, and SVG.

## Design rules

- Canvas #fff8f4 / #fffdf9; white cards; warm tinted #fff7ed highlights; orange #ea580c accents; dark #292524 text and warm subtle borders.
- Editorial serif headings and readable system sans body with deliberate Chinese fallbacks. Do not fetch web fonts. Exact font embedding needs licensing and size review.
- Use a fluid laptop-friendly layout capped at 1600px, with 24px outer gutters, a 24px column gap and a fixed 240px desktop command/contents panel. The reading card fills the remaining width. Keep the panel aligned inside the page gutter, 24px from the top, with viewport-bounded height and its own scrolling. Below 800px, place the unified panel above the document rather than overlaying text. No fixed document heights; wide tables scroll locally, never overflow the page.
- Render all content sections as native `details`/`summary`, initially expanded, with keyboard-visible focus and plus/minus indicators. The fixed panel includes bilingual Expand all, Collapse all and Back to top controls. Contents links open the destination before scrolling; hash navigation must also open it.
- Expand every section before printing and restore the reading state afterward. Download exports reset sections to expanded, include both languages and retain working controls. Native section toggles remain usable without JavaScript; bulk controls are hidden without it.
- Distinct title, short subtitle, metadata chips, sectional hierarchy and callouts. Callout purpose uses a label rather than color alone. Accent-on-white must meet readable contrast; use darker orange for small text.
- Put all commands inside the unified floating panel. Use one Chinese/English switch at the top, not two language buttons. Download, Print, Expand all, Collapse all and Back to top use inline SVG icons with 44px hit targets, translated hover/focus tips and accessible names. Contents links are individual bordered rounded cards with warm backgrounds and hover/focus highlighting. Do not duplicate commands in a separate page toolbar. Avoid teacher annotations, sharing/authoring workflows and fake application menus.
- Semantic headings, lists, captions/table headers, visible keyboard focus, reduced-motion respect and print CSS. Print hides toolbar/navigation and uses white backgrounds; avoid forcing large whole sections onto a single page.

## Portability

Replace prototype dependencies such as Tailwind CDN, Google Fonts, and icon-font services with embedded CSS, inline SVG, and system fonts. Resource links can require network, but rendering never should. If images are necessary, embed approved assets with bilingual descriptions; do not automatically fetch student-data images or expiring private attachments.

## Content variants

Lesson: overview, learning goals, preparation as supported, steps, deliverables, source-derived success checklist, reflection/resources as supported.

Meeting: summary, decisions, milestones/actions, uncertainty, next steps. Never force source content into every possible section: absent information stays absent or labeled unknown.
