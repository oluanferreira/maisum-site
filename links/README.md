# +UM central v4 (preview only)

User requested stronger navigation clarity and premium 3D illustrations, citing Apple, Inter and iFood. Preserve Pinterest's compact editorial craft while making destination names explicit.

## Design and assets
Three primary destinations: explore experiences, register an establishment, and influencer partnership. Existing accounts grouped separately, support in its own section. A consistent original 3D illustration sheet supports the four intents. All functional copy is live accessible HTML; illustrations are decorative.
DM Sans and Cormorant Garamond: SIL Open Font License in fonts/.
3D artwork: generated specifically for +UM, stored in links/assets/brand-3d.png, approximately 1.2 MB shared once across all four illustrations. No external font/image requests. No fake product, partner, reviews, prices or commission rates. No animation loops.

## Behavior and scope
Seven audience links work without JavaScript. WhatsApp only opens prepared messages. A single validated explicit affiliate follows the existing same-origin homepage and checkout flow; no global affiliate or storage. Homepage, sales page, main and production are untouched. Preview is noindex.

## Validation
python -m unittest discover -s tests -v
node --check links/central.js && node --test tests/central.test.cjs
python tests/browser_smoke.py (Playwright Chromium)
Six viewports, minimum touch targets, images, fonts, no overflow, no runtime errors, no-JS, keyboard, affiliate round-trip and intercepted WhatsApp checks.
