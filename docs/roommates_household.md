# Roommates household ("דירת שותפים") - feature design

Status: **V1.1, design only.** Nothing here is built until all seven V1 core completion
criteria pass (CLAUDE.md rule 10). The feature name is a working title.

## 1. Why
A student who cooks alone buys full packages for one person and throws part of them away.
Flatmates who plan together can pool the same ingredients, buy each package once, make fewer
shopping trips and plan the week in one go. The product promise stays the same (save money and
time); the household makes the saving larger.

## 2. Decisions
| Topic | Decision |
|---|---|
| Scope | V1.1. V1 core keeps only "how many people do you cook for" |
| Sharing | Per meal: each meal is `together` or `solo`; one combined shopping list covers all |
| Dietary conflicts | Shared meals use the **strictest common rules**, filtered in code (rule 4) |
| Joining | Invite code/link; every roommate signs in with their own Auth0 account and fills their own profile |
| Size | Up to 4 members per household (first estimate) |
| Location | One household location; nearest branch of each chain to it (rule 5 unchanged) |

## 3. Model
- **Household**: id, invite code, owner, location, members.
- **Member**: own Auth0 user, own profile (body, training, taste, sensitivities, habits) and own
  budget (target + flexibility).
- **Planned meal**: day, meal type, mode `together | solo`, participants (a subset of members).
  A `solo` meal has one participant.

## 4. Rules (all calculated in code, never by the AI; rule 3)

### 4.1 Strictest-common filter for a shared meal
For the participants of a meal, the allowed set is what is left after combining everyone's rules:

- allergens: the **union** of all participants' allergens is forbidden
  (`gluten, dairy, nuts, eggs, soy`; same tags as `Ingredient.allergens`);
- vegetarian / vegan: applies if **any** participant is (`is_meat_or_fish`, `is_animal_product`);
- kashrut: applies if **any** participant keeps kashrut: no meat with dairy, no non-kosher
  categories (`kashrut`, `non_kosher`). Product certification is still not verified.

Recipes that pass the filter are the only ones the AI can pick from (rule 4). The AI never
sees or decides anything about who is allowed what.

If no recipe passes for a shared meal, the app says so and offers `solo` for that meal.

### 4.2 Portions and nutrition
Quantities scale with the number of participants. Calories and protein are still computed per
member against that member's own target, from the catalogue (rule 3).

### 4.3 One combined shopping list
1. Sum each ingredient across all meals and all members.
2. Round **up to the package size once** (`package_size`, `package_unit`).
3. Pantry staples stay off the list; items with no price in any branch file are excluded from
   every chain's total and marked "price unknown" (rule 6).

### 4.4 Chain ranking and prices
Rank the three chains for the pooled basket, each from the nearest branch to the household
location, with the file date (rule 5).

### 4.5 Budget and cost split
- Each member keeps a personal ceiling = target + flexibility (rule 7).
- Household ceiling = sum of the members' ceilings.
- Shared items are split by participating portions; solo items are charged to the member.
- If the plan cannot fit, the app says so, for the household and per member.

### 4.6 Saving metric
Household saving = (sum of each member's individual basket, rounded separately) minus (the
pooled basket, rounded once). The existing baseline stays: average of the three chains for the
same basket (rule 8).

## 5. Privacy
Members see which restrictions were applied to a shared meal ("no dairy, vegetarian"), not whose
they are. Each member edits only their own profile.

## 6. Flow
1. A student creates a household and gets an invite code.
2. Roommates sign in with their own account, enter the code and fill their own profile.
3. Any member marks each meal `together` or `solo` and picks the participants.
4. The app builds the plan (4.1-4.2), the combined list (4.3), the chain ranking (4.4) and the
   cost split (4.5).
5. They shop at the chosen chain and tick items off together.

## 7. Edge cases
- A member leaves: their solo meals are removed; shared meals are re-filtered and re-priced.
- A member has not finished their profile: their meals cannot be `together` until they do.
- No recipe satisfies the strict filter: say so; offer `solo`.
- Members with very different budgets: costs are split by portions, ceilings stay personal.

## 8. Open technical question
Streamlit has no shared storage. Households need a small shared database (for example
SQLite or Postgres). Not decided; revisit after V1 core.

## 9. Tests to write when built
- Strict-common filter, parametrised over allergen, vegetarian/vegan and kashrut combinations
  (extends completion criterion 6).
- Pooled rounding buys fewer or equal packages than the sum of individual rounding.
- Cost split sums exactly to the basket total.
- A household of one gives the same result as the single-user flow.

## 10. Test data
All sample data used for design or tests is labelled test data (rule 1).
