# +UM central: Pinterest direction (preview only)

Compact illustrated banner links, serif typography and layered original food photography. No homepage, sales page, Instagram or production changes.

## Sources
Visual references supplied by the user: Pinterest pins 1123929650779638508 and 1046172188462176860. Design language only, no third-party brand/portrait/copy reused.
Photography: existing official +UM repository. Burger image is the Tati Burguer photograph with background removed; original remains untouched. Other visual compositions are HTML/CSS, not a purported live app screen.
Fonts: Cormorant Garamond and DM Sans, SIL Open Font License included.

## Behavior
All seven audience paths work without JavaScript. WhatsApp opens a prepared message without sending. Influencer commission is a conversation, no rate or automation promised. An explicitly supplied, single valid affiliate parameter is passed only to the same-origin homepage for the existing checkout flow. No global affiliate, cookies or local storage.

## Checks
python -m unittest discover -s tests -v
node --check links/central.js && node --test tests/central.test.cjs
python tests/browser_smoke.py (requires Playwright Chromium)

Preview is noindex; remove preview-only indexing restriction only after approval for production.
