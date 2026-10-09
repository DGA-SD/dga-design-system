# Tokens: DGA

Themes: light, dark (first = light)

## color

| token | light | dark | usage |
|---|---|---|---|
| `surface` | `#ffffff` | `#150f36` | Page and slide background. Dark theme is a deep DGA navy, not black. |
| `surface-subtle` | `#fafafa` | `#1e154c` | Alternating page bands, sidebars, table stripes. |
| `surface-muted` | `#f2f1f1` | `#2a2160` | Input fills, image placeholders, quiet panels. ink-muted does NOT reach 4.5:1 here in light theme; use ink-secondary. |
| `ink` | `#1e154c` | `#edebf5` | Primary text and headings on surface, surface-subtle and surface-muted. In light theme it is DGA navy, the site's main text colour. |
| `ink-secondary` | `#444444` | `#b9b4d6` | Body copy in dense UI and article paragraphs, on surface and surface-subtle. |
| `ink-muted` | `#707070` | `#a39dc8` | Dates, captions, metadata; on surface and surface-subtle only (4.95:1 / 6.38:1). |
| `line` | `#dcdcdc` | `#3a3170` | Hairline dividers and card outlines (decorative, not meaning-bearing). |
| `line-strong` | `#c1c1c1` | `#6e66a6` | Control borders (source value). Light #c1c1c1 is 1.8:1 on white, below the 3:1 floor for control borders: kept exact from dga.or.th; pair inputs with a label and the focus ring. |
| `navy` | `#1e154c` | `#1e154c` | DGA navy (the 'A' of the logo). Footer, hero bands, cover and section-divider slides. Same in both themes. |
| `on-navy` | `#ffffff` | `#ffffff` | Text and icons on a navy fill (16.6:1). |
| `orange` | `#f05223` | `#f05223` | DGA orange, the brand colour (logo 'DG'). Fills, large headings 24px+ (3.54:1 on white), graphics, and text on navy (4.69:1). Never small body text on white. |
| `orange-strong` | `#da3c0c` | `#ff7a4d` | Primary buttons, links, active nav text, focus ring. Text on surface (4.53:1 light / 7.06:1 dark). |
| `on-orange` | `#ffffff` | `#150f36` | Label on an orange-strong fill (4.53:1 light / 7.06:1 dark). |
| `orange-soft` | `#fff5f0` | `#3b1a14` | Tint behind active nav items and highlighted rows. Source pairs orange-strong text here at 4.22:1 (below 4.5:1 for 14.72px nav text): kept exact; bold 19px+ passes. |
| `focus` | `{orange-strong}` | `{orange-strong}` | Focus ring: 2px solid, 2px offset. 4.53:1 on white, 7.06:1 on dark surface. |
| `link` | `{orange-strong}` | `{orange-strong}` | Inline links and 'อ่านต่อ' read-more links. |
| `success` | `#2e7d32` | `#6bcb77` | Completed / on-track status. Always with a word or icon, never colour alone. |
| `warning` | `#b45309` | `#f2b14c` | At-risk / pending status. Always with a word or icon. |
| `danger` | `#b42318` | `#ff8a80` | Error / off-track. Keep visibly distinct from brand orange by pairing with an icon and the word. |
| `info` | `#1d6fb8` | `#6fa8ff` | Informational notices and neutral status. |
| `chart-1` | `#1e154c` | `#b9b4d6` | First data series (navy). Charts in decks and reports. |
| `chart-2` | `#f05223` | `#f05223` | Second data series / the highlighted series (orange). |
| `chart-3` | `#8a84b8` | `#8a84b8` | Third series (navy tint). 3.46:1 on white, 5.27:1 on dark: fine for marks, label it directly. |
| `chart-muted` | `#c1c1c1` | `#3a3170` | 'Other' / baseline / comparison bars. Carries no meaning on its own. |

## shadow

| token | light | dark | usage |
|---|---|---|---|
| `shadow-sm` | `0 2px 8px 0 rgba(0,0,0,0.06)` | `0 2px 8px 0 rgba(0,0,0,0.3)` | Sticky header, small raised controls. |
| `shadow-card` | `0 16px 24px 0 rgba(73,104,126,0.16)` | `0 16px 24px 0 rgba(0,0,0,0.4)` | News and service cards (site value). |
| `shadow-overlay` | `0 8px 32px 0 rgba(0,0,0,0.18)` | `0 8px 32px 0 rgba(0,0,0,0.5)` | Menus, dialogs, popovers. |
| `shadow-cta` | `0 4px 16px 0 rgba(218,60,12,0.4)` | `0 4px 16px 0 rgba(0,0,0,0.5)` | Hover on the primary orange button only. |

## spacing

| token | value | usage |
|---|---|---|
| `space-1` | `4px` | Icon-to-text gaps. |
| `space-2` | `8px` | Tight stacks: tag padding, meta rows. |
| `space-3` | `12px` | Button vertical padding, list gaps. |
| `space-4` | `16px` | Nav item vertical padding (site), card inner gaps. |
| `space-5` | `20px` | Nav item horizontal padding (site), button horizontal padding. |
| `space-6` | `24px` | Card padding, grid gutters. |
| `space-8` | `32px` | Between blocks inside a section. |
| `space-12` | `48px` | Section padding on mobile; slide margin minimum. |
| `space-16` | `64px` | Section padding on desktop. |
| `space-24` | `96px` | Hero padding; slide outer margin at 1920x1080. |

## radius

| token | value | usage |
|---|---|---|
| `radius-sm` | `6px` | Buttons, inputs, tags (site value). |
| `radius-md` | `12px` | Cards, images, panels (the site's most common radius). |
| `radius-lg` | `20px` | Hero media, feature panels. |
| `radius-pill` | `100px` | Pills and chips (site value). |
| `radius-round` | `50%` | Circular icon buttons (carousel arrows, back-to-top). |

## type

- `--font-sans`: `Prompt, "Noto Sans Thai", system-ui, sans-serif`
- `--font-reading`: `Sarabun, Prompt, "Noto Sans Thai", sans-serif`

### Web (family `sans`)

| style | size | line | weight | usage |
|---|---|---|---|---|
| `.display` | 56px | 64px | 600 | Hero headline, one per page. |
| `.h1` | 40px | 52px | 600 | Page title. |
| `.section-title` | 32px | 32px | 600 | Home-page section headings in orange, exactly as dga.or.th. Line height 1.0 is for ONE line only; wrap to h2 metrics if it breaks. |
| `.h2` | 32px | 44px | 600 | Multi-line section headings. |
| `.h3` | 24px | 34px | 600 | Card and sub-section titles. |
| `.h4` | 20px | 30px | 500 | News-card titles, small headings. |
| `.body` | 16px | 24px | 400 | Default UI and web copy (site value). |
| `.nav` | 14.72px | 19.872px | 500 | Main navigation items (site value). |
| `.label` | 14px | 20px | 500 | Buttons, tags, form labels. |
| `.caption` | 12px | 18px | 400 | Dates, captions, footnotes (site value). |

### Article (family `reading`)

| style | size | line | weight | usage |
|---|---|---|---|---|
| `.article-lead` | 21px | 34px | 400 | Standfirst under an article title. |
| `.article-body` | 18px | 32px | 400 | Long-form reading text in Sarabun. Max line length ~70 characters (680px). |
| `.article-quote` | 24px | 38px | 500 | Pull quotes, in Prompt. |

### Slides (family `sans`)

| style | size | line | weight | usage |
|---|---|---|---|---|
| `.slide-hero` | 72px | 84px | 600 | Title slide headline at 1920x1080. |
| `.slide-title` | 48px | 62px | 600 | Content-slide title at 1920x1080. |
| `.slide-subtitle` | 30px | 44px | 400 | Subtitles and kicker lines. |
| `.slide-body` | 26px | 40px | 400 | Bullets and body on slides. Never below 24px. |
| `.slide-stat` | 120px | 120px | 700 | One big number per slide (e.g. Waseda ranking). |
