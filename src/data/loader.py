"""Load raw M5 data tables."""

from pathlib import Path

import pandas as pd


def load_raw_m5_data(
    raw_data_path: Path,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Load the raw M5 data tables.

    Args:
        raw_data_path (Path): Path to the directory containing the raw M5 CSV files.

    Returns:
        tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]: The
            `sales_train_validation`, `calendar`, and `sell_prices` DataFrames,
            respectively.
    """
    sales_train_validation = pd.read_csv(raw_data_path / "sales_train_validation.csv")
    calendar = pd.read_csv(raw_data_path / "calendar.csv")
    sell_prices = pd.read_csv(raw_data_path / "sell_prices.csv")

    return sales_train_validation, calendar, sell_prices
