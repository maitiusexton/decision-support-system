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

Checklist:
- [x] Extract appropriate pipeline functionality from `02_data_pipeline.ipynb` into `src/`
- [x] Establish basic tests for the data pipeline
- [x] Establish reusable data-loading functionality
- [x] Define the initial structure for analytical/modeling code
- [x] Confirm the project is ready to begin forecasting

### Next Session
- Determine what code from `02_data_pipeline.ipynb` should be extracted into `src/`.

## 2026-08-13

### Completed
- Worked under Issue #9 on branch `feature/9-extract-data-pipeline`.
- Extracted the validated `item_store_day` transformation from `02_data_pipeline.ipynb` into reusable project code at `src/data/pipeline.py`.
- Implemented `build_item_store_day()` to:
  - Melt `sales_train_validation` from wide to long format.
  - Join `calendar` on `d` to add `date` and `wm_yr_wk`.
  - Convert `d` from the `d_X` string format to `int64`.
  - Join `sell_prices` on `(item_id, store_id, wm_yr_wk)` to add `sell_price`.
  - Calculate `daily_revenue` as `units_sold * sell_price`.
  - Enforce the expected output dtypes and column order.
- Added `many_to_one` merge validation for both the calendar and sell-price joins.
- Added `pytest==9.1.1` as a development dependency and installed the project in editable mode.
- Confirmed the project package can be imported through the installed `src` layout.
- Added `tests/test_pipeline.py` with three tests:
  - Happy-path validation of the complete pipeline.
  - Rejection of duplicate `calendar.d` keys.
  - Rejection of duplicate `(item_id, store_id, wm_yr_wk)` sell-price keys.
- All three automated tests pass.
- Created `03_pipeline_verification.ipynb` to verify the extracted pipeline against the existing validated `data/processed/item_store_day.parquet`.
- Confirmed that the new pipeline output exactly matches the existing Parquet output in shape, column order, dtypes, and values.
- Confirmed the generated analytical dataset contains 58,327,370 rows and the expected eight-column schema.
- Left `02_data_pipeline.ipynb` unchanged.

### Key Takeaways
- The reusable pipeline now lives in `src/` rather than the exploratory notebook.
- The pipeline remains a DataFrame-in/DataFrame-out transformation; raw file loading is intentionally kept separate.
- The existing Parquet dataset can serve as a full-data regression reference when validating changes to the pipeline.
- Basic automated testing is now established for the data pipeline.

### Next Session
- Establish reusable data-loading functionality for the raw M5 tables.
- Determine whether any additional pipeline infrastructure is justified by concrete requirements.
- Continue preparing the project for forecasting.

## 2026-08-13

### Completed
- Worked under Issue #11 on branch `feature/11-raw-data-loader`.
- Added `src/data/loader.py` with a reusable `load_raw_m5_data()` function for loading the three raw M5 tables.
- Used `pathlib.Path` for the raw data directory and kept the loader interface aligned with `build_item_store_day()`.
- Added `tests/test_loader.py` using pytest's `tmp_path` fixture and Pandas testing utilities.
- Confirmed the loader returns the `sales_train_validation`, `calendar`, and `sell_prices` DataFrames in the expected order.
- Verified the loader against the actual M5 raw files.
- Confirmed the full test suite passes with four tests.
- Adopted an 88-character Python line-length standard and configured Black as the formatter.

### Key Takeaways
- Raw-data loading is now separated from the transformation pipeline.
- `load_raw_m5_data()` provides the reusable input boundary for `build_item_store_day()`.
- The reusable data foundation now includes raw-data loading, item-store-day transformation, and basic automated testing.

### Next Session
- Define the initial structure for analytical/modeling code.
- Determine whether any additional pipeline infrastructure is justified by concrete requirements.
- Continue preparing the project for forecasting.

## 2026-08-14

### Completed
- Began development and evaluation of a one-step-ahead forecasting baseline.
- Defined the evaluation period as the final 365 days of the available historical data.
- Implemented a lag-1 baseline where each item-store's previous day's demand is used to predict the next day's demand.
- Calculated overall MAE and RMSE and verified the calculations using scikit-learn.
- Added `scikit-learn==1.9.0` and `matplotlib==3.11.1` as project dependencies.
- Built an item-store-level evaluation summary containing:
  - Mean daily demand
  - Standard deviation of demand
  - MAE
  - RMSE
- Analyzed the distributions of demand and forecast error across item-store combinations.
- Defined relative MAE as item-store MAE divided by mean daily demand to compare forecast performance across different demand scales.
- Found that relative forecast error generally decreases as mean daily demand increases.
- Investigated 464 item-store combinations with relative MAE exactly equal to `2.0` and found that they are characterized by low, intermittent demand.
- Determined why relative MAE reaches exactly `2.0` for these intermittent-demand series: an isolated sale causes the lag-1 baseline to miss the sale itself and then incorrectly predict that sale on the following zero-sales day.
- Found a strong, approximately linear relationship between demand variability and baseline MAE.

### Key Takeaways
- Overall MAE alone does not adequately describe baseline performance because item-store demand levels vary substantially.
- Item-store-level evaluation provides substantially more insight into forecast behavior than a single aggregate metric.
- The lag-1 baseline performs particularly poorly relative to demand for low-volume and intermittent-demand series.
- Higher-demand item-store combinations generally have lower relative forecast errors.
- The median relative MAE is approximately `1.313`, meaning the median item-store's MAE is about 131% of its mean daily demand.
- Baseline MAE is strongly associated with the underlying variability of an item-store's demand.
- The intermittent-demand analysis identified a specific structural weakness of the lag-1 baseline rather than simply identifying poor metric values.

### Medium-Term Goal
Establish and understand a credible forecasting baseline before moving to more sophisticated forecasting approaches.

Checklist:
- [x] Define the initial one-step-ahead forecasting problem
- [x] Implement a lag-1 forecasting baseline
- [x] Establish a 365-day evaluation period
- [x] Calculate and validate baseline MAE and RMSE
- [x] Begin item-store-level baseline diagnostics
- [x] Finish evaluating and summarizing the lag-1 baseline
- [ ] Establish the benchmark that subsequent forecasting approaches should beat
- [ ] Determine the next forecasting approach based on what the baseline analysis reveals

### Next Session
- Continue evaluating the lag-1 forecasting baseline.
- Determine whether any additional baseline diagnostics are necessary.
- Summarize what the baseline analysis has taught us about the demand series and baseline behavior.
- Establish the benchmark that subsequent forecasting approaches should beat.
- Determine the next forecasting approach based on what the baseline analysis reveals.

## 2026-08-18

### Completed
- Worked under Issue #15 on branch `feature/15-baseline-analysis`.
- Created `05_baseline_analysis.ipynb` to continue analysis of the lag-1 forecasting baseline.
- Recreated the 365-day lag-1 evaluation dataset and item-store-level performance summary.
- Measured demand sparsity using the proportion of zero-demand days for each item-store combination.
- Found substantial demand sparsity across the evaluation period:
  - Mean zero-demand rate was approximately 59.7%.
  - Median zero-demand rate was approximately 64.1%.
  - 66.6% of item-store combinations had zero demand on at least half of evaluation days.
- Examined the relationship between zero-demand rate and relative MAE and found that relative forecast error generally increases as demand becomes more sparse, although sparsity alone does not explain performance.
- Measured how frequently demand switches between zero and nonzero states and compared this with relative MAE.
- Determined that demand-state switch rate alone does not clearly distinguish good and poor lag-1 performance.
- Compared representative best- and worst-performing item-store combinations by relative MAE.
- Found that the lag-1 baseline closely tracks relatively continuous demand but performs poorly for highly intermittent demand with long periods of zero sales and occasional demand events.

### Key Takeaways
- Demand sparsity is a major characteristic of the item-store-level forecasting problem rather than an edge case.
- The lag-1 baseline is most useful when recent demand provides meaningful information about next-day demand.
- Highly intermittent demand exposes a structural weakness of lag-1 forecasting: the model tends to miss isolated demand when it occurs and then predict that demand one day too late.
- Neither zero-demand rate nor demand-state switch rate alone fully explains forecast performance.
- Examining individual demand series provides important context that aggregate error metrics cannot capture.
- The baseline diagnostics are now sufficient to inform selection of the next forecasting approach.

### Next Session
- Establish the lag-1 benchmark that subsequent forecasting approaches should beat.
- Determine the next forecasting approach based on the baseline findings.
- Begin implementing and evaluating the next forecasting approach.
