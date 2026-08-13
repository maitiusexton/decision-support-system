import pandas as pd

from data.loader import load_raw_m5_data


def test_load_raw_m5_data(tmp_path):
    sales_train_validation = pd.DataFrame(
        {"item_id": ["item_1"], "store_id": ["store_1"]}
    )
    calendar = pd.DataFrame({"d": ["d_1"], "date": ["2011-01-29"]})
    sell_prices = pd.DataFrame({"item_id": ["item_1"], "store_id": ["store_1"]})

    sales_train_validation.to_csv(tmp_path / "sales_train_validation.csv", index=False)
    calendar.to_csv(tmp_path / "calendar.csv", index=False)
    sell_prices.to_csv(tmp_path / "sell_prices.csv", index=False)

    loaded_sales, loaded_calendar, loaded_prices = load_raw_m5_data(tmp_path)

    pd.testing.assert_frame_equal(loaded_sales, sales_train_validation)
    pd.testing.assert_frame_equal(loaded_calendar, calendar)
    pd.testing.assert_frame_equal(loaded_prices, sell_prices)
