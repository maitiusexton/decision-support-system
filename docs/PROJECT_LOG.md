# Project Log

## 2026-08-03

### Completed
- Created repository
- Wrote initial README
- Downloaded M5 dataset
- Created project structure

### Next
- Explore dataset
- Understand table relationships

## 2026-08-05

### Completed
- Explored all three M5 tables (`sales_train_validation`, `calendar`, `sell_prices`).
- Documented the purpose, grain, key columns, and unknowns for each.
- Investigated `wm_yr_wk` and determined it represents Walmart retail weeks rather than calendar weeks.
- Explored price change behavior across item-store combinations.

### Key Takeaways
- `sales_train_validation` is the historical demand table.
- `calendar` maps day IDs to dates and calendar/business context.
- `sell_prices` contains weekly prices by item and store.
- `store_id` determines `state_id`.
- `dept_id` determines `cat_id`.
- `wm_yr_wk` connects `calendar` to the weekly pricing data; the full `sell_prices` join uses `item_id`, `store_id`, and `wm_yr_wk`.

### Next Session
- Build a complete mental model of how the three tables relate.
- Identify primary keys and join paths.
- Sketch the data model before moving into forecasting.

## 2026-08-10

### Completed
- Established the grain and unique key of each raw table:
  - `sales_train_validation`: one item-store, `(item_id, store_id)`
  - `calendar`: one day, `d`
  - `sell_prices`: one item-store-week, `(item_id, store_id, wm_yr_wk)`
- Validated that each of these keys is unique in its respective table.
- Determined that `sales_train_validation` needs to be unpivoted from wide to long format.
- Established the join path:
  - Sales → Calendar using `d`
  - Sales + Calendar → Sell Prices using `(item_id, store_id, wm_yr_wk)`
- Defined the target analytical grain as one item-store-day observation.
- Defined the initial analytical dataset fields:
  - `item_id`
  - `store_id`
  - `d`
  - `date`
  - `wm_yr_wk`
  - `units_sold`
  - `sell_price`
  - `daily_revenue`
- Decided to keep the raw tables separate and generate the analytical dataset through a reproducible pipeline.
- Decided to create a static Parquet copy of the processed dataset as a convenience artifact, while keeping the pipeline as the source of truth.
- Estimated the fully expanded daily dataset at approximately 58.3 million rows.

### Next Session
- Build the item-store-day data pipeline.
- Determine appropriate Pandas dtypes for the analytical dataset.
- Implement the transformation and joins.
- Validate the resulting dataset.
- Write the processed dataset to Parquet.