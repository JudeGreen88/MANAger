# Roommates household ("דירת שותפים") - feature design

Status: **V1.1, design only.** Nothing here is built until all seven V1 core completion
criteria pass (CLAUDE.md rule 10). The feature name is a working title.

## 1. Why
A student who cooks alone buys full packages for one person and throws part of them away.
Flatmates who plan together can pool the same ingredients, buy each package once, make fewer
shopping trips and plan the week in one go. The promise stays the same: plan money **and** time
well. The household makes the saving larger.

## 2. Decisions
| Topic | Decision |
|---|---|
| Scope | V1.1. V1 core: "how many people" only multiplies quantities for one profile |
| Sharing | Per meal: `together` or `solo`; one combined shopping list covers all |
| Dietary conflicts | Shared meals use the **strictest common rules**, filtered in code (rule 4) |
| Portions | Each participant picks small / regular / large for each shared meal |
| Cost of leftover package share | Split by use (weighted portions) |
| Saving metric | "Same plan, shopping separately" vs pooled basket; named separately from chain saving |
| Plan ownership | Owner builds the plan; members mark meals until the plan is locked |
| Joining | Invite code that expires, owner approval, consent text; own Auth0 account and profile |
| Budget | Only the household total ceiling is binding; each member's share is shown, not enforced |
| Membership | One household per user at a time; owner leaving hands over ownership |
| Size | Up to 4 members (first estimate) |
| Location | One household location; nearest branch of each chain to it (rule 5 unchanged) |
| Cross-contact | Disclaimer only; filtering covers shared meals |

## 3. Model
- **Household**: id, invite code (with expiry), owner, location, members, plan status
  (`open | locked`).
- **Member**: own Auth0 user, own profile (body, training, taste, sensitivities, habits) and
  own budget (target + flexibility). Belongs to at most one household at a time.
- **Planned meal**: day, meal type, mode `together | solo`, participants (a subset of members),
  portion size per participant (`small | regular | large`). A `solo` meal has one participant.
  A shared meal needs every participant to have chosen that meal type in their own profile
  (US6).

## 4. Rules (all calculated in code, never by the AI; rule 3)

### 4.1 Strictest-common filter for a shared meal
For the participants of a meal, combine everyone's rules:

- allergens: the **union** of all participants' allergens is forbidden
  (`gluten, dairy, nuts, eggs, soy`; same tags as `Ingredient.allergens`);
- vegetarian / vegan: applies if **any** participant is (`is_meat_or_fish`, `is_animal_product`);
- kashrut: applies if **any** participant keeps kashrut: no meat with dairy, no non-kosher
  categories (`kashrut`, `non_kosher`). Product certification is still not verified.

Only recipes that pass are given to the AI (rule 4). The AI never decides who may eat what.
If no recipe passes for a shared meal, the app says so and offers `solo` for that meal.

### 4.2 Portions and nutrition
- Portion sizes are weights, first estimate: small 0.75, regular 1.0, large 1.5.
- Ingredient quantities for a shared meal = recipe quantities for one regular portion x the sum
  of the participants' weights.
- Calories and protein are computed per member from the catalogue for that member's portion
  and shown against that member's own target (rule 3). If a member's portion leaves them short
  of the target, the app shows it; it does not hide the gap.

### 4.3 One combined shopping list
1. Sum each ingredient across all meals and all members.
2. Round **up to the package size once** (`package_size`, `package_unit`).
3. Pantry staples stay off the list; items with no price in any branch file are excluded from
   every chain's total and marked "price unknown" (rule 6).

### 4.4 Chain ranking and prices
Rank the three chains for the pooled basket, each from the nearest branch to the household
location, with the file date (rule 5).

### 4.5 Budget and cost split
- Household ceiling = sum of the members' ceilings (each = target + flexibility, rule 7).
  **Only the household ceiling is binding:** if the pooled basket exceeds it, the app says the
  plan cannot fit.
- Each member's share is shown, with a notice when it is above that member's own ceiling. It is
  not blocked, because shares depend on how the group splits packages.
- Cost split: each item's price is split in proportion to each member's use of it (weighted
  portions across all meals, shared and solo). The unused part of a package is split in the
  same proportion.
- Shares sum exactly to the basket total; rounding differences go to the owner by agreement
  with the group (first estimate: owner pays the agorot remainder).

### 4.6 Savings, named separately
- **Chain saving**: cheapest chain vs the average of the three chains for the same basket
  (rule 8). Unchanged.
- **Household saving**: the same plan bought separately by each member (each member's items
  rounded to packages alone) minus the pooled basket rounded once, at the same chain.
  It measures only the effect of buying together.

## 5. Privacy, security and consent
- Invite code expires (first estimate: 48 hours) and every join request needs the owner's
  approval. The owner can remove a member.
- On joining, a member sees a consent text: "Your dietary restrictions will shape shared meals."
- Members see which restrictions applied to a shared meal ("no dairy, vegetarian"), not whose
  they are. With 2-4 people this is not a guarantee of anonymity; the consent text says so.
- Each member edits only their own profile. Allergies and sensitivities are sensitive data:
  keep them minimal and delete them when a member leaves.

## 6. Flow
1. A student creates a household and gets an invite code.
2. Roommates sign in with their own account, enter the code, accept the consent text and wait
   for the owner's approval; then they fill their own profile.
3. Members mark meals `together` or `solo`, choose participants and portion sizes, until the
   owner builds the plan (the plan becomes `locked`).
4. The app builds the plan (4.1-4.2), the combined list (4.3), the chain ranking (4.4) and the
   cost split (4.5). The owner can unlock to change it.
5. They shop at the chosen chain and tick items off. Check-off is refreshed on a short timer or
   by hand in V1.1; live sync is later.

## 7. Edge cases
- A member leaves: their solo meals are removed; shared meals are re-filtered and re-priced;
  their sensitivity data is deleted. If the owner leaves, ownership passes to the longest-
  standing member.
- A member has not finished their profile: their meals cannot be `together` until they do.
- No recipe satisfies the strict filter: say so; offer `solo`.
- A member moves to another flat: they leave and join the other household (one at a time).
- Different budgets: the household ceiling binds; each share is shown.

## 8. Cross-contact disclaimer
The filter covers shared meals only. A "just me" meal of another member can contain an
allergen that stays in the same kitchen and on the same shopping list; the same holds for
meat and dairy separation. The app tells the household this plainly, as it already does for
product kashrut. Members with a severe allergy must check labels and agree on kitchen rules.

## 9. Open technical question
Streamlit has no shared storage. Households need a small shared database (for example SQLite or
Postgres). Not decided; revisit before building V1.1.

## 10. Tests to write when built
- Strict-common filter, parametrised over allergen, vegetarian/vegan and kashrut combinations
  (extends completion criterion 6).
- Pooled rounding buys fewer or equal packages than the sum of individual rounding.
- Cost shares sum exactly to the basket total, including the unused part of a package.
- Portion weights: quantities scale with the sum of weights.
- A household of one gives the same result as the single-user flow.

## 11. Open items (not decided)
- Portion weights, invite expiry and household size are first estimates to validate with users.
- The shared database (see section 9).

Completion criteria H1-H6 and build-order step 7 are defined in `CLAUDE.md`. In short: strict
filter test, pooled list no worse than separate lists, shares sum to the total, a household of
one equals the single-user flow, database chosen first, and the join/consent controls tested.

## 12. Test data
All sample data used for design or tests is labelled test data (rule 1).
