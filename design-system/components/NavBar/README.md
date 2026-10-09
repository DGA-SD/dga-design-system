# NavBar

The site header is a white bar with the DGA logo on the left, the main menu on the right and `shadow-sm` beneath.

**Consumer provides:** the logo (`assets/Logos/dga-logo.webp`, 48px high, with the Thai organisation name as `alt`), 4–7 menu links, and `aria-current="page"` on the active link.

- Items use `nav` type (14.72px/500) with `space-4` × `space-5` padding, as on the site.
- The active item takes an `orange-soft` fill with `orange-strong` text. This source pair is 4.22:1, so keep weight 500 or heavier.
- In the dark theme the bar turns navy and the logo gets a white plate automatically (bundle.css).
- On mobile, collapse to a menu button (`dga-btn--icon`).
