import hashlib
import logging

import pandas as pd

logger = logging.getLogger(__name__)


def transform_data(transformed: pd.DataFrame) -> pd.DataFrame:
    df = transformed.copy()

    logger.info("Cleaning dimensions and generating operational IDs")

    df["time"] = df["time"].astype(str).str.strip().astype(int)
    df["value"] = pd.to_numeric(df["value"], errors="coerce").astype("Float64")

    missing_values = df["value"].isna().sum()
    if missing_values > 0:
        logger.warning(f"Coerced {missing_values} invalid value strings into null")

    if "flag" not in df.columns:
        df["flag"] = pd.NA

    def generate_uid(row: pd.Series) -> str:
        unique_string = (
            f"{row['freq']}_{row['sector']}_{row['na_item']}_{row['geo']}_"
            f"{row['unit']}_{row['direct']}_{row['time']}"
        )
        return hashlib.sha256(unique_string.encode("utf-8")).hexdigest()

    df["id"] = df.apply(generate_uid, axis=1)

    return df[["id", "freq", "sector", "na_item", "geo", "unit", "direct", "time", "value", "flag"]]
