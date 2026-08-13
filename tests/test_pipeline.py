import pandas as pd
import pytest
from pandas.errors import MergeError
from data.pipeline import build_item_store_day


@pytest.fixture
def m5_data():
    sales_train_validation = pd.DataFrame(
        {
            "item_id": ["item_1", "item_2"],
            "store_id": ["store_1", "store_1"],
            "d_1": [10, 5],
            "d_2": [20, 10],
        }
    )

    calendar = pd.DataFrame(
        {
            "d": ["d_1", "d_2"],
            "date": ["2011-01-29", "2011-01-30"],
            "wm_yr_wk": [11101, 11101],
        }
    )

    sell_prices = pd.DataFrame(
        {
            "store_id": ["store_1", "store_1"],
            "item_id": ["item_1", "item_2"],
            "wm_yr_wk": [11101, 11101],
            "sell_price": [2.00, 3.00],
        }
    )

    return sales_train_validation, calendar, sell_prices


def test_build_item_store_day(m5_data):
    """Confirms that valid M5 inputs produce the expected item-store-day dataset (happy-path test)."""
    sales_train_validation, calendar, sell_prices = m5_data

    result = build_item_store_day(
        sales_train_validation,
        calendar,
        sell_prices,
    )

    expected = pd.DataFrame(
        {
            "item_id": ["item_1", "item_2", "item_1", "item_2"],
            "store_id": ["store_1", "store_1", "store_1", "store_1"],
            "d": [1, 1, 2, 2],
            "date": pd.to_datetime(
                ["2011-01-29", "2011-01-29", "2011-01-30", "2011-01-30"]
            ),
            "wm_yr_wk": [11101, 11101, 11101, 11101],
            "units_sold": [10, 5, 20, 10],
            "sell_price": [2.00, 3.00, 2.00, 3.00],
            "daily_revenue": [20.00, 15.00, 40.00, 30.00],
        }
    )

    pd.testing.assert_frame_equal(result, expected)


def test_build_item_store_day_rejects_duplicate_calendar_keys(m5_data):
    """Confirms that a duplicate calendar.d value causes the pipeline to reject the
    input rather than silently producing duplicated/multiplied rows."""
    sales_train_validation, calendar, sell_prices = m5_data

    # Duplicate the first calendar row to violate the expected unique `d` key
    calendar = pd.concat(
        [calendar, calendar.iloc[[0]]],
        ignore_index=True,
    )

    # The calendar merge should reject the duplicate key via `many_to_one` validation
    with pytest.raises(MergeError):
        build_item_store_day(
            sales_train_validation,
            calendar,
            sell_prices,
        )


def test_build_item_store_day_rejects_duplicate_price_keys(m5_data):
    """Confirms that a duplicate value for the primary key in `sell_prices` (`item_id`, `store_id`, `wm_yr_wk`)
    causes the pipeline to reject the input rather than silently producing duplicated/multiplied rows."""
    sales_train_validation, calendar, sell_prices = m5_data

    # Duplicate the first sell_prices row to violate the expected unique (`item_id`, `store_id`, `wm_yr_wk`) key
    sell_prices = pd.concat(
        [sell_prices, sell_prices.iloc[[0]]],
        ignore_index=True,
    )

    # The sell_prices merge should reject the duplicate key via `many_to_one` validation
    with pytest.raises(MergeError):
        build_item_store_day(
            sales_train_validation,
            calendar,
            sell_prices,
        )
