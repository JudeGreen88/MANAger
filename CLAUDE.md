# MANAger (מנה + manager)

Source of truth for scope: `MANAger_Product_Specification.md`. If this file and the spec disagree, stop and ask the team.

## Product
Mobile-first web app for Jerusalem students (19-30, dorms/shared flats, tight budget). It builds a weekly meal plan from a short profile, produces one shopping list, and ranks Shufersal, Rami Levy and Osher Ad from cheapest to most expensive for that basket. The user shops in person at the nearest branch. No delivery, no ordering. Main promise: save money.

## Stack
Python, Streamlit, Claude API, Auth0 login, shared GitHub repo. No separate FastAPI backend until Streamlit hits a real limit. UI language: English in V1 core (Hebrew RTL in V1.1).

## Scope
**V1 core** (build this semester):
- Auth0 sign-in; saved profile (US1)
- Onboarding: body, training, taste, sensitivities, eating habits, budget (US2-US4)
- Location by GPS or address/neighbourhood (US5)
- Weekly plan for chosen meals (breakfast/lunch/dinner), simple recipes (<=30 min, <=8 ingredients), reusing base ingredients across recipes (US6)
- Calories and protein on the card, carbs and fat in details, daily/weekly summary vs. target (US7)
- Swap a single meal (US8)
- Chain ranking from each chain's nearest-branch price file, with distance (US9)
- One combined shopping list for the chosen chain, rounded up to package sizes, no pantry staples (oil, salt, sugar, spices), price per item and total (US10)
- Check-off list for use in the store (US11)

**V1.1** (only after all completion criteria pass): list download, meal history, "now" suggestion, private-label vs. brands, over-budget options (keep / cheaper brands / replace 1-2 dishes), Hebrew RTL, promotions/seasons/holidays.

**Later / out of scope**: pantry items at home; other plan durations; other cities or chains; families/non-students; splitting a basket across chains; separate backend; delivery or pick-up; medical advice.

## Non-negotiable rules
1. Test data is always labelled as test data.
2. The AI never invents prices or products. It only picks recipes from the human-validated ingredient catalogue (~150 items mapped to product codes per chain).
3. All totals, quantities, nutrition values, package rounding and filtering are calculated in code from the catalogue, never by the AI, and are tested.
4. Allergen (gluten, dairy, nuts, eggs, soy, meat, fish...), vegetarian/vegan and kashrut filtering is done in code before recipes reach the AI. Kashrut is a recipe-level rule: no meat with dairy, no non-kosher categories (pork, seafood). Product certification is not verified; the app tells the user to check the label.
5. Price each chain from the file of its nearest branch, never a chain-wide price. Show the file date. Files must be no older than 7 days; fall back to the last valid file with its date shown.
6. An item with no price in any of the three branch files is excluded from every chain's total and marked "price unknown", so the ranking compares identical baskets. Show how many items are excluded.
7. Budget ceiling = target budget + chosen flexibility (strict 0%, flexible up to 10%). If the plan cannot fit, say so clearly (V1 core).
8. Savings baseline = average of the three chains for the same basket.
9. Nutrition values are shown as estimates, from one official source (candidate: Israeli Ministry of Health database, to verify).
10. Nothing outside V1 core is built before all seven completion criteria pass.

## Completion criteria (definition of done)
1. Sign-up to priced shopping list in under 5 minutes.
2. Every ingredient in every generated recipe exists in the catalogue: 0 unmatched.
3. Totals, quantities and nutrition come from code; a test checks them.
4. Prices come from files no older than 7 days, and the date is shown.
5. The plan stays within the budget ceiling, or the app says it cannot.
6. No recipe contains an ingredient conflicting with a marked sensitivity or diet (including meat+dairy for kashrut); an automated test checks it.
7. Runs on demo day from a public URL in a phone browser.

## Build order (PROPOSED; the spec mentions six phases but does not list them, team to confirm)
1. Ingredient catalogue and tags (allergens, meat/dairy/pareve, nutrition per 100 g, package sizes).
2. Price-file pipeline and chain ranking (test the open-source price-file library first).
3. Profile and calculation engine (calorie/protein targets, budget ceiling, filters) with tests.
4. AI plan generation restricted to the catalogue, plus single-meal swap.
5. Streamlit UI: Auth0, questionnaire, location, plan, ranking, shopping list, check-off.
6. Hardening and deploy: criteria tests, public URL, phone check.

## Decision log
| Topic | Decision |
|---|---|
| Stores | One chain per basket |
| Branches | Nearest branch of each chain, by GPS or address |
| Meals | User picks breakfast/lunch/dinner for one week |
| Language | English V1 core, Hebrew V1.1 |
| Over budget | V1 core: say it cannot fit; V1.1: three options |
| Rounding | Up to package size, in code |
| Missing prices | Excluded everywhere, marked "price unknown" |
| Kashrut | Recipe-level rule |
| Savings baseline | Average of the three chains |

**Open**: cost per weekly plan (estimate after 50 generations); nutrition data source; testing the open-source price-file library.

## Team and conventions
Roles: price data; catalogue and AI prompt; interface and integration. Keep commits small, add a decision-log line whenever a decision changes. Test command: _to add once the repo is set up_.
