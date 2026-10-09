# Button

Use a button to start an action or go to the next step, with at most one **primary** (orange) button per view.

**Consumer provides:** an `<a>` or `<button>` with class `dga-btn` plus one variant, a short verb label (for example "ลงทะเบียน" or "ดาวน์โหลด") and, optionally, an inline 16px SVG icon.

| Variant | Class | When |
|---|---|---|
| Primary | `dga-btn--primary` | The main action. `orange-strong` fill, `on-orange` label, `shadow-cta` on hover. |
| Secondary | `dga-btn--secondary` | Alternatives. Navy outline on `surface`. |
| On navy | `dga-btn--on-navy` | The action inside a navy band or footer. |
| Link | `dga-btn--link` | "อ่านต่อ →" read-more links on cards and lists. |
| Icon | `dga-btn--icon` | Carousel arrows and back-to-top. Round, and must have an `aria-label`. |

- Do write labels as verb-first Thai without full stops, with radius `radius-sm` and the 2px `focus` ring.
- Don't place two primary buttons side by side, use `orange` (#F05223) as a fill behind small labels (3.54:1), or make an icon-only button without an `aria-label`.
