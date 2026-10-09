# NewsCard

The news and article card from the dga.or.th home page is a 16:9 image, a category badge, a title clamped to three lines, a Thai-calendar date and a "อ่านต่อ →" link.

**Consumer provides:** an image (`<img class="dga-card__media">`, 16:9, with `alt`), one badge, the headline, a date in the Buddhist Era (for example "25 ก.ย. 2569") and a link.

- Cards have `radius-md` and `shadow-card` and no border. Lay them out three or four across with `space-6` gutters.
- The whole card may be the link, but keep the visible "อ่านต่อ" for clarity.
- Don't put more than one badge on a card or write an excerpt longer than two lines.
