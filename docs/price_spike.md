# Price-file spike (build-order step 2a)

Status: **not run yet.** This file holds the plan, the candidates and the runbook. Fill in the
results section after running it.

## Goal
Show that real branch price files can price a 15-20 item sample basket from `data/catalogue.csv`
for Shufersal, Rami Levy and Osher Ad, and measure how far apart the chains are.

## Candidates (from a web search; licences and maintenance NOT verified)
| Library | What it is | Notes |
|---|---|---|
| `il-supermarket-scraper` (PyPI; GitHub: erlichsefi/israeli-supermarket-scarpers) | Raw price-file downloader for chains on the gov.il roster; Docker option | Some chain sites are blocked from outside Israel; only the current snapshot is available; fork maintenance looks uneven |
| `israeli-prices` (PyPI; GitHub: rxradar/israeli-prices) | Typed client, one interface for most roster chains, GTIN helper for cross-chain comparison | Announced Aug 2026, so young; check licence and recent commits |
| `korenLazar/supermarket-scraping` | Promotions-focused scraper | Probably not what we need (promotions are V1.1) |

Check for each: licence, last commit, open issues, which chains and file types (price vs
price-full), and whether it needs to run from an Israeli IP.

## Findings so far (2026-11-22, attempt on the development Mac, Python 3.9.6)
- `israeli-prices`: `pip` found no distribution (no versions listed for Python 3.9); not tested.
- `il-supermarket-scraper` 1.1.2 installs, and has scrapers for `SHUFERSAL`, `RAMI_LEVY`,
  `OSHER_AD`. Its `pip show` license field says **CUSTOM**: read the repo licence before use.
  It pulls heavy dependencies (playwright, pymongo).
- It **does not run on Python 3.9**: it calls `anext`, which exists only in Python 3.10+. No
  files were downloaded. **Use Python 3.10 or newer** (3.11/3.12 recommended).
- API notes: `ScarpingTask(enabled_scrapers=["SHUFERSAL", ...], files_types=["STORE_FILE"],
  output_configuration={"output_mode": "disk", "base_storage_path": "<dir>"}, multiprocessing=1)`,
  then `.start(limit=N)` and `.join()`; run it from a script file with an
  `if __name__ == "__main__":` guard (macOS multiprocessing). Scraper names are strings.
- Next: fetch `STORE_FILE` per chain to find a Jerusalem branch id, then fetch that branch's
  `PRICE_FULL_FILE` with `file_name_regex`.

## Runbook (run in your own terminal, in Israel)
Use a separate virtualenv and a fresh empty directory. Downloaded price files are untrusted
data: do not run anything from inside that directory, and read them with `python -I`.

```bash
mkdir -p ~/price_spike/work && cd ~/price_spike
python3 -m venv venv && source venv/bin/activate
pip install israeli-prices        # or: pip install il-supermarket-scraper
pip show israeli-prices           # note Version and License
```

Then follow the chosen library's README to fetch the **latest price file of one Jerusalem
branch per chain** (store ids differ per chain). Save the files under `~/price_spike/work`.
Never commit raw files; `data/prices_cache/` is git-ignored.

## What to measure
1. For 15-20 catalogue items, match by `name_he`/`name_en` (and barcode where possible):
   how many are found per chain?
2. File date of each branch file (completion criterion 4: no older than 7 days).
3. Parse problems: encoding, missing prices, units (per kg vs per package).
4. Basket total per chain for the matched items, and the spread vs the average of the three
   chains (tests the "saving" assumption; rule 8).
5. Items missing in any chain (these would be "price unknown" everywhere; rule 6).

## Decision after the spike
| Result | Next step |
|---|---|
| >= 90% of sample items priced in all 3 chains | Go: build step 2 pipeline on this library |
| 60-90% | Widen manual mapping or shrink the catalogue to the items that match |
| < 60%, or a chain is unavailable | Reconsider the library, or the 3-chain promise |

## Results (run 2026-11-22, Python 3.12, il-supermarket-scraper 1.1.2)
This is a partial run: **2 of 3 chains**, name matching only, no real basket yet.

- **Library:** `il-supermarket-scraper` 1.1.2 works on Python 3.12 (Homebrew `python@3.12`).
  `israeli-prices` 0.2.0 (MIT) also installs on 3.12; not used yet. The scraper's licence field
  is "CUSTOM": read it before depending on it.
- **Download works from this machine:** the Rami Levy file came via FTP
  (`url.retail.publishedprices.co.il`), Shufersal via its portal (`prices.shufersal.co.il`).
- **Branch lists (store files):** all 3 chains have Jerusalem branches (city code 3000):
  Shufersal 23, Rami Levy 11, Osher Ad 3. Store files are dated 2026-11-20 to 22.
- **Price files obtained:**
  | Chain | Branch | Items | Newest price update |
  |---|---|---|---|
  | Shufersal | store 002, "Shufersal Sheli Agron", Jerusalem | 8,094 | 2026-11-20 |
  | Rami Levy | store 001, Talpiot, Jerusalem | 12,958 | 2026-11-21 |
  | Osher Ad | **not obtained** (the file fetched was store 001, not a Jerusalem branch) | - | - |
  Files generated 2026-11-22, so within the 7-day limit (criterion 4).
- **Spread:** over 3,808 barcodes present in both files, Rami Levy Talpiot is on average about
  **9% cheaper** than Shufersal Sheli Agron (median ratio 0.909). This is a different branch
  format per chain (Sheli is a small-format Shufersal), so it is only a first signal, not a basket.
- **Catalogue matching (18 items, by Hebrew name keyword):** every item except bread matched at
  least one product in both files, but **keyword matching is too noisy to use**: "eggs" matched
  egg noodles, "onion" matched onion soup, "salt" matched seasoned sunflower seeds, "tomato" matched
  sauces. Bread found nothing; chicken breast found few. Only a human-validated barcode mapping
  (the ~150-item catalogue) will work, as the spec says.
- **Same-barcode overlap between the two chains:** about 10-30 barcodes for staples such as pasta,
  rice, tuna, chickpeas, tahini, cottage cheese and tofu. Fresh produce (tomato, cucumber, onion)
  and bread/chicken are mostly weighted or bakery items without a shared barcode.

### Problems and risks found
1. **Produce, bread and meat** need a rule: weighted items (`bIsWeighted`, price per kg) and items
   without a shared barcode are not comparable by barcode. Decide: map them to a representative
   weighted item per chain, or exclude them ("price unknown", rule 6).
2. **Osher Ad Jerusalem file** was not retrieved: filtering by store id found nothing, and the
   library listing may be paginated. Needs another attempt (try stores 003, 026, 028 with a
   different filter, or `israeli-prices`).
3. **File names** differ per chain (`PriceFull<chain>-<store>-<subchain>-<date>`); store ids are
   zero-padded; sub-chain matters (Shufersal store 002 appears as `-002-013-`).
4. **Heavy dependencies** (playwright, pymongo) and a custom licence; check before adopting.
5. Files are large (5-11 MB each, 8k-13k items): cache per branch (spec: cache Jerusalem files).

### Recommendation
**Go, with conditions.** Real branch files are reachable, fresh and show a visible price spread
between chains. Next: (a) get an Osher Ad Jerusalem file, (b) build the barcode mapping by hand
for 15-20 staples, (c) price a real basket in all 3 chains, (d) decide the rule for produce,
bread and meat, (e) review the library licence or switch to `israeli-prices`.
