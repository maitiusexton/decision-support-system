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
- `wm_yr_wk` is the key connecting `calendar` and `sell_prices`.

### Next Session
- Build a complete mental model of how the three tables relate.
- Identify primary keys and join paths.
- Sketch the data model before moving into forecasting.