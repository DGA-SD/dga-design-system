The visual and verbal system of the Digital Government Development Agency (สำนักงานพัฒนารัฐบาลดิจิทัล (องค์การมหาชน) · สพร. · DGA), taken from dga.or.th and the DGA logo. Use it for three surfaces: **presentations**, **articles** and **websites**. Two colours carry the brand, DGA orange and DGA navy, over plenty of white, and everything is set in Prompt.

## Content fundamentals

**Voice.** DGA speaks as a public servant: confident about what it delivers, and warm toward the citizen. Lead with what the person gets, then say which system does it. Real headlines from the site:

- "One Stop Service ใกล้ขึ้น ข้อมูลถึงกัน เอกสารไม่ซ้ำ ประชาชนไม่ต้องถ่ายสำเนา"
- "เรื่องนี้ต้องแจ้งที่ไหน? เมื่อรัฐออกแบบบริการให้ประชาชนไม่ต้องหาคำตอบเอง"
- "Digital Government in Action"

**Rules.**

- Write Thai first. English is for section labels that are already English on the site (Policy & Regulation, Standard, Open Government Data) and for international audiences.
- Name the organisation "DGA" in headlines and "สำนักงานพัฒนารัฐบาลดิจิทัล (องค์การมหาชน) (สพร.)" at first formal mention. Keep product names exactly as written: ทางรัฐ, Citizen Portal, BizPortal, GDX, DG-Link, TDGA, DIGI.
- Headlines state an outcome or ask the citizen's question. Avoid slogans with no subject.
- Numbers are concrete and sourced: "58 เอกสารสำคัญ", "อันดับที่ 17 ของโลก (Waseda 2025)". Use Arabic numerals.
- Buttons and links are short verbs: "อ่านต่อ", "ดูทั้งหมด", "ดาวน์โหลด", "ลงทะเบียน".
- Formal register (ภาษาราชการที่อ่านง่าย): no slang, no exclamation marks in body copy, and no emoji in any output.
- Royal and state-mourning announcements follow official protocol and never use brand colours. Set them in greyscale.

## Visual foundations

**Colour.** White `surface` dominates. `navy` and `orange` are the two brand fills; everything else is support.

- Set text in `ink` (navy), secondary copy in `ink-secondary`, and metadata in `ink-muted` (on `surface` or `surface-subtle` only).
- `orange` (#F05223) is the logo orange. Use it for fills, graphics and headings **24px and larger**. It reads 4.69:1 on `navy`, so orange text on navy is fine at any size. Never use it for small text on white (3.54:1).
- `orange-strong` (#DA3C0C) is the working orange. Use it for primary buttons, links, active navigation and the `focus` ring. Put labels on it in `on-orange`.
- Use `navy` blocks for the footer, hero bands, title slides and section dividers, with text in `on-navy`.
- `orange-soft` tints the active navigation item and highlighted rows.
- Status colours (`success`, `warning`, `danger`, `info`) always come with a word or icon. `danger` must never be the only thing telling it apart from brand orange.
- For charts, use `chart-1` (navy) for the main series and `chart-2` (orange) for the one to look at. Add `chart-3` if needed, and put everything else in `chart-muted`. Label series directly rather than with a legend where possible.
- The **Dark (navy)** theme swaps white for deep navy (`surface` #150F36). Use it for keynote decks and dark website sections; the tokens hold contrast in both themes.
- No gradients, no purple, and no colour outside these tokens.

**Type.** Everything is set in **Prompt** (Google Fonts, Thai + Latin, weights 400/500/600/700), as on dga.or.th. Long-form article text uses **Sarabun**, the Thai government reading face (an addition: dga.or.th has no long-form style).

- Web: `display` → `h1` → `h2` / `section-title` → `h3` → `h4` → `body` → `label` → `caption`. Use `section-title` (32px, 600, orange) exactly as the home page does, on one line only; Thai marks clip at line-height 1.0 across two lines, so switch to `h2` when it wraps.
- Articles: `article-lead`, then `article-body` (Sarabun 18/32) at a maximum measure of 680px, with `article-quote` for pull quotes.
- Slides (1920×1080): `slide-hero`, `slide-title`, `slide-subtitle`, `slide-body` (never below 24px) and `slide-stat` for one big number.
- Weights: 600 for headings, 500 for navigation and labels, 400 for text. 700 is for `slide-stat` only.

**Spacing and layout.** Use a 4px base (`space-1` … `space-24`).

- Web: content width 1200px, 12 columns with `space-6` gutters, section padding `space-16` (`space-12` on mobile). Service tiles run three across (Policy & Regulation · Standard · มติ ครม.) and news runs three or four across.
- Slides: outer margin `space-24`, one idea per slide, title at top-left, and the logo bottom-right at 56px tall (except on the title slide).
- Articles: a single 680px column, centred, with images allowed to break out to 960px.

**Shape and depth.** Buttons and inputs take `radius-sm` (6px), cards and images `radius-md` (12px), feature panels `radius-lg`, chips `radius-pill`, and carousel and back-to-top buttons `radius-round`. Cards lift with `shadow-card` and do not use borders. The primary button gets `shadow-cta` on hover. Menus and dialogs use `shadow-overlay`.

**States.** Hover darkens a fill by one step or raises the shadow. Focus is a 2px solid `focus` ring with a 2px offset, on every interactive element. Disabled elements drop to 40% opacity and have no shadow.

**Imagery.** Use real photography of Thai citizens, officials and DGA events, cropped to `radius-md` corners. Screens of ทางรัฐ and other services appear inside plain device frames. Do not use stock handshake or "digital globe" clichés or AI-generated people.

**Accessibility.** dga.or.th offers text resizing and display modes; keep layouts working at 200% text. Two source values miss WCAG and are kept exact but flagged. `line-strong` on white is 1.8:1, so always label inputs. `orange-strong` on `orange-soft` is 4.22:1, so active navigation text should be 500 weight or heavier and never smaller than `nav`.

## Iconography

- The site uses **Font Awesome** (solid set) for UI icons and small custom SVGs for carousel arrows. Use Font Awesome 6 Free Solid, single-colour, in `ink` or `orange-strong`, at 16/20/24px. Icons appear next to a label, not in place of one.
- Do not use emoji or Unicode symbols as icons.

## Logo

`assets/Logos/dga-logo.webp` is the official DGA logo (orange "DG" with circuit ends, navy "A", "DIGITAL GOVERNMENT DEVELOPMENT AGENCY" beneath), 339×194, taken from dga.or.th.

- Place it on `surface` (white) only. On navy or photographs, sit it on a white plate with `space-4` padding and `radius-md` corners.
- Leave clear space around it equal to the height of the "A". Minimum height is 48px on screen and 56px on slides.
- Never recolour, outline, stretch, rotate or redraw it. There is no reversed (white) version in this system yet; request an official file from DGA Corporate Communications before making one.

## Using this system

- **Websites.** Load `components/bundle.css` (it imports Prompt and Sarabun) after `tokens.css`, then use the `dga-` classes: NavBar, Button, SectionHeader, NewsCard, ServiceTile, Badge, StatBlock and Footer.
- **Articles.** Wrap the body in `.dga-prose`; add `Callout` blocks for key facts and pull quotes.
- **Presentations.** Build from the SlideTitle, SlideContent and SlideSection layouts. Use a light theme for working decks and the dark (navy) theme for keynotes. Keep to one orange accent per slide.
