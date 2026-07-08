import hashlib
import logging

import pandas as pd

logger = logging.getLogger(__name__)


def transform_data(transformed: pd.DataFrame) -> pd.DataFrame:
    required_fields = ["freq", "sector", "na_item", "geo", "unit", "direct", "time"]

    missing_cols = set(required_fields) - set(transformed.columns)
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")

    null_counts = transformed[required_fields].isnull().sum()
    if null_counts.any():
        raise ValueError(f"Null values found in required fields:\n{null_counts[null_counts > 0]}")

    dfc = transformed.copy()

    logger.info("Cleaning dimensions and generating operational IDs")

    dfc["time"] = dfc["time"].astype(str).str.strip().astype(int)
    dfc["value"] = pd.to_numeric(dfc["value"], errors="coerce").astype("Float64")

    missing_values = dfc["value"].isna().sum()
    if missing_values > 0:
        logger.warning(f"Coerced {missing_values} invalid value strings into null")

    if "flag" not in dfc.columns:
        dfc["flag"] = pd.NA

    def generate_sha256(row: pd.Series) -> str:
        unique_string = (
            f"{row['freq']}_{row['sector']}_{row['na_item']}_{row['geo']}_"
            f"{row['unit']}_{row['direct']}_{row['time']}"
        )
        return hashlib.sha256(unique_string.encode("utf-8")).hexdigest()

    dfc["id"] = dfc.apply(generate_sha256, axis=1)

    return dfc[["id", "freq", "sector", "na_item", "geo", "unit", "direct", "time", "value", "flag"]]
