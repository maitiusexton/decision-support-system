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

## 2026-08-11

### Completed
- Built the item-store-day data pipeline:
  - Melted `sales_train_validation` from wide to long format using Pandas `melt()`.
  - Retained `item_id` and `store_id` as identifier columns.
  - Joined `calendar` on `d` to add `date` and `wm_yr_wk`.
  - Joined `sell_prices` on `(item_id, store_id, wm_yr_wk)` to add `sell_price`.
  - Calculated `daily_revenue` as `units_sold * sell_price`.
- Validated the resulting dataset:
  - Confirmed the `(item_id, store_id, d)` primary key remained unique.
  - Confirmed the expected eight columns.
  - Confirmed the expected number of rows: 58,327,370.
  - Validated missing `sell_price` values and confirmed they correspond to item-store combinations without a price record for the relevant week.
  - Confirmed `daily_revenue` calculations for rows with non-null prices.
- Converted `d` from string to integer and confirmed the remaining columns had appropriate dtypes.
- Reordered columns with primary key fields first.
- Persisted the completed dataset to `data/processed/item_store_day.parquet`.
- Verified the persisted Parquet file with PyArrow and confirmed the expected schema.

### Next Session
- Set up a project virtual environment with reproducible dependencies.
- Resolve the Pandas/PyArrow compatibility issue.
- Continue with the next data pipeline step.

## 2026-08-12

### Completed
- Created a project virtual environment using Python 3.11.2.
- Established reproducible project dependencies in `pyproject.toml`:
  - `pandas==2.3.3`
  - `pyarrow==25.0.1`
  - `ipykernel==7.3.0` as a development dependency.
- Configured VS Code to use the project virtual environment for Jupyter notebooks.
- Re-ran the full item-store-day pipeline in the project environment.
- Verified the original Pandas Parquet write operation using `DataFrame.to_parquet()`.
- Verified the original Pandas Parquet read operation using `pd.read_parquet()`.
- Confirmed the original Pandas/PyArrow compatibility issue could not be reproduced in the clean project environment.
- Verified that a fresh virtual environment could install the project and all dependencies directly from `pyproject.toml`.
- Kept `requirements.txt` blank, with `pyproject.toml` serving as the project's dependency source of truth.

### Medium-Term Goal
Turn the working data pipeline into a reusable project structure.

- [ ] Extract appropriate pipeline functionality from `02_data_pipeline.ipynb` into `src/`
- [ ] Establish reusable data-loading functionality
- [ ] Establish basic tests for the data pipeline
- [ ] Define the initial structure for analytical/modeling code
- [ ] Confirm the project is ready to begin forecasting

### Next Session
- Determine what code from `02_data_pipeline.ipynb` should be extracted into `src/`.
