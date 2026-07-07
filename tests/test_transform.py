import hashlib

import pandas as pd

from src.etl_pipeline.transform import transform_data


def test_transform_data_converts_time_and_numeric_values():
    input_df = pd.DataFrame(
        {
            "freq": ["A"],
            "sector": ["B"],
            "na_item": ["C"],
            "geo": ["D"],
            "unit": ["E"],
            "direct": ["F"],
            "time": ["2020 "],
            "value": ["10.5"],
            "flag": ["p"],
        }
    )

    result = transform_data(input_df)

    assert result["time"].tolist() == [2020]
    assert result["value"].tolist() == [10.5]
    assert result["flag"].tolist() == ["p"]


def test_transform_data_coerces_invalid_values_to_nan():
    input_df = pd.DataFrame(
        {
            "freq": ["A", "A"],
            "sector": ["B", "B"],
            "na_item": ["C", "C"],
            "geo": ["D", "D"],
            "unit": ["E", "E"],
            "direct": ["F", "F"],
            "time": ["2021", "2022"],
            "value": ["12", "not-a-number"],
        }
    )

    result = transform_data(input_df)

    assert result.loc[0, "value"] == 12.0
    assert pd.isna(result.loc[1, "value"])


def test_transform_data_generates_a_deterministic_id_and_preserves_columns():
    input_df = pd.DataFrame(
        {
            "freq": ["A"],
            "sector": ["B"],
            "na_item": ["C"],
            "geo": ["D"],
            "unit": ["E"],
            "direct": ["F"],
            "time": ["2023"],
            "value": ["7"],
            "flag": ["p"],
        }
    )

    result = transform_data(input_df)

    expected_id = hashlib.sha256(
        b"A_B_C_D_E_F_2023"
    ).hexdigest()

    assert result.loc[0, "id"] == expected_id
    assert list(result.columns) == [
        "id",
        "freq",
        "sector",
        "na_item",
        "geo",
        "unit",
        "direct",
        "time",
        "value",
        "flag",
    ]
