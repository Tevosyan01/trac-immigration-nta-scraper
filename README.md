# TRAC Reports — New Proceedings Filed (NTA) Scraper

Scrapes time-series values from **TRAC Reports**:  
https://tracreports.org/phptools/immigration/ntanew/

The script opens the page, applies the selected filters, and reads **FY / Value** from the bar chart via a **hover tooltip**.  
Results are printed to the console and automatically written to `logs/run.txt`.

> Stack: Selenium + undetected-chromedriver, ActionChains hover, robust waits (WebDriverWait).

## What it collects
- Pairs: **`FY → Value`** (sorted by year)

## Filters (entered in the console)
- **Nationality** (e.g., `All`, `Mexico`, `Cuba`)
- **Immigrant County** (e.g., `Dallas County, TX`)
- **How Long in U.S.** (e.g., `All-Mexico`, `Not Known`, `Between 3 and 4 years`)

> Enter the **exact names as shown on the site** (copy from the UI) so selectors match.
