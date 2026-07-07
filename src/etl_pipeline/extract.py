import logging

import pandas as pd
from pyjstat import pyjstat
from requests import PreparedRequest

logger = logging.getLogger(__name__)


def extract_data(url: str, params: dict | None = None) -> pd.DataFrame:
    logger.info("Fetching and parsing JSON-stat dataset")

    req = PreparedRequest()
    req.prepare_url(url, params)
    full_url = req.url

    dataset = pyjstat.Dataset.read(full_url)

    df = dataset.write("dataframe", naming="id")
    logger.info(f"Successfully extracted {len(df)} records")
    return df
