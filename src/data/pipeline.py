"""Data transformation pipeline for the Decision Support System."""

import pandas as pd


def build_item_store_day(
    sales_train_validation: pd.DataFrame,
    calendar: pd.DataFrame,
    sell_prices: pd.DataFrame,
) -> pd.DataFrame:
    """
    Build the item-store-day analytical dataset from the raw M5 data tables.

    Args:
        sales_train_validation (pd.DataFrame): Daily unit sales in wide format,
            with one row per item-store combination.
        calendar (pd.DataFrame): Calendar data containing the date and Walmart
            retail week corresponding to each day.
        sell_prices (pd.DataFrame): Weekly selling prices by item-store
            combination.

    Returns:
        pd.DataFrame: Item-store-day dataset containing daily unit sales,
            calendar information, selling price, and daily revenue.
    """
    cols_to_unpivot = sales_train_validation.columns[
        sales_train_validation.columns.str.startswith("d_")
    ]

    item_store_day = pd.melt(
        sales_train_validation,
        id_vars=["item_id", "store_id"],
        value_vars=cols_to_unpivot,
        var_name="d",
        value_name="units_sold",
    )
    item_store_day = pd.merge(
        item_store_day,
        calendar[["d", "date", "wm_yr_wk"]],
        how="left",
        on="d",
        validate="many_to_one",
    )

    item_store_day["d"] = item_store_day["d"].str[2:].astype("int64")

    item_store_day = pd.merge(
        item_store_day,
        sell_prices,
        how="left",
        on=["item_id", "store_id", "wm_yr_wk"],
        validate="many_to_one",
    )

    item_store_day["daily_revenue"] = (
        item_store_day["units_sold"] * item_store_day["sell_price"]
    )

    # Enforce dtypes
    item_store_day = item_store_day.astype(
        {
            "item_id": "object",
            "store_id": "object",
            "d": "int64",
            "date": "datetime64[ns]",
            "wm_yr_wk": "int64",
            "units_sold": "int64",
            "sell_price": "float64",
            "daily_revenue": "float64",
        }
    )

    # Enforce column order
    isd_cols = [
        "item_id",
        "store_id",
        "d",
        "date",
        "wm_yr_wk",
        "units_sold",
        "sell_price",
        "daily_revenue",
    ]
    item_store_day = item_store_day[isd_cols]

    return item_store_day
