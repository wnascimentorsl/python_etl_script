import logging

import pandas as pd
from pyjstat import pyjstat

logger = logging.getLogger(__name__)


def extract_data(url: str) -> pd.DataFrame:
    logger.info("Fetching and parsing JSON-stat dataset from Eurostat")
    dataset = pyjstat.Dataset.read(url)
    df = dataset.write("dataframe", naming="id")
    logger.info(f"Successfully extracted {len(df)} records")
    return df
