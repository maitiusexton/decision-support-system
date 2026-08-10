# Chat Context

Use this document as the primary context when continuing this project.

## Project

Decision Support System

Build an end-to-end Decision Support System that helps inventory planners make better purchasing decisions under uncertainty using the M5 Walmart dataset.

The long-term vision is:

Business Understanding
→ Data Understanding
→ Demand Forecasting
→ Inventory Optimization
→ Scenario Analysis
→ Decision Dashboard

The project should be treated as a software product, not a Kaggle notebook.

---

## My Goals

This project exists to help me become the kind of data scientist I want to be.

Priority goals:

- Become stronger at practical data science.
- Learn software engineering best practices.
- Build one flagship portfolio project instead of many unrelated projects.
- Learn by reasoning through problems instead of copying code.
- Develop intuition before implementation.

Long-term, I want to work on a team with experienced data scientists who can mentor me. I value clean engineering, impactful business problems, and building decision-support systems more than chasing state-of-the-art ML.

---

## How I'd Like You to Help

Act as a senior data scientist and mentor.

Default behavior:

- Give objectives instead of code.
- Ask guiding questions.
- Let me struggle a little.
- Only provide code when I ask or when I'm genuinely stuck.
- Challenge my thinking.
- Treat this like a real software project.
- When providing Markdown intended for direct copy/paste into `.md` files, use a fenced code block so the literal Markdown syntax is preserved.

Avoid repeatedly saying things like:

"No models.
No feature engineering.
No optimization."

Keep responses conversational.

---

## Repository Workflow

- One GitHub Issue per feature.
- One feature branch per issue.
- One Pull Request per feature.
- Squash merge into `main`.

---

## Current Status

### Completed

- Repository initialized.
- Project structure created.
- M5 dataset downloaded.
- Git workflow established.
- Issue #1 created.
- Branch `feature/1-data-exploration` created.
- Explored `sales_train_validation`, `calendar`, and `sell_prices`.
- Documented the purpose, structure, grain, and key fields of each table.
- Investigated `wm_yr_wk` and determined it represents Walmart retail weeks.
- Explored price change behavior across item-store combinations.
- Established and validated the relationships between the three raw tables.
- Confirmed the unique keys:
  - `sales_train_validation`: `(item_id, store_id)`
  - `calendar`: `d`
  - `sell_prices`: `(item_id, store_id, wm_yr_wk)`
- Determined that `sales_train_validation` must be unpivoted from wide to long format to create daily observations.
- Defined the target analytical grain as one item-store-day observation, uniquely identified by `(item_id, store_id, d)`.
- Decided to keep the raw tables separate and create the analytical dataset through a reproducible data pipeline.
- Decided to keep the first analytical dataset minimal.
- Estimated the fully expanded daily dataset at approximately 58.3 million rows.
- Decided to use Parquet for the static processed dataset and keep the pipeline as the source of truth.

### Raw Table Metadata

| Table | Grain | Primary / Unique Key |
|---|---|---|
| `sales_train_validation` | One item-store | `(item_id, store_id)` |
| `calendar` | One day | `d` |
| `sell_prices` | One item-store-week | `(item_id, store_id, wm_yr_wk)` |

### Key Relationships

- `sales_train_validation.d` → `calendar.d`
- `sales_train_validation.(item_id, store_id, wm_yr_wk)` → `sell_prices.(item_id, store_id, wm_yr_wk)`

### Target Analytical Dataset

The initial `item_store_day` dataset will contain:

```text
item_id
store_id
d
date
wm_yr_wk
units_sold
sell_price
daily_revenue