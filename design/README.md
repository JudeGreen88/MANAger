# MANAger UI design (Stitch prototype)

Mobile UI screens generated with Google Stitch from `MANAger_Product_Specification.md` (V1 core flow).
Stitch project: "MANAger" (private, owner's account).

**All numbers, prices, products and store names on these screens are mock content.**
They are *test data* (CLAUDE.md rule 1) and are not taken from the ingredient catalogue or any
price file. Real totals and rankings must come from code (rules 2-3).

## Files
- `DESIGN.md` - design system exported from Stitch (colors, type, shapes, components).
- `stitch/chain-ranking.html` - US9: three chains ranked, distance, price-file date.
- `stitch/shopping-list.html` - US10/US11: check-off list, "price unknown" notice, total.
  (Oil was removed: pantry staples are excluded.)
- `stitch/onboarding-step3.html` - US5/US6: location and meals to plan.

## Not exported yet
Sign in, onboarding step 1, budget (step 2) and weekly plan were generated in Stitch but their
file IDs were not returned, so they are only in the Stitch project.
Screenshots (PNG) are not saved here either.

## Notes
- The HTML files load Tailwind and fonts from CDNs, so open them online.
- Design reference only; the real app is Streamlit (see CLAUDE.md).
