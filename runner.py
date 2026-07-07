import logging
import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine

from src.etl_pipeline.extract import extract_data
from src.etl_pipeline.load import load_data
from src.etl_pipeline.transform import transform_data

logging.basicConfig(
    level  = logging.INFO,
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

load_dotenv(Path(__file__).resolve().parent / ".env")

EUROSTAT_URL = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/nasa_10_nf_tr"
DATABASE_URL = os.getenv("DATABASE_URL")

def main() -> None:
    if not DATABASE_URL:
        logging.warning("DATABASE_URL is not set. Exiting pipeline.")
        return

    params = {
        "format": "JSON",
        "time": ["2021", "2022", "2023"],
        "geo": "IE",
    }

    engine = create_engine(DATABASE_URL)
    raw_data = extract_data(EUROSTAT_URL, params)
    transformed_data = transform_data(raw_data)
    load_data(transformed_data, engine)

if __name__ == "__main__":
    main()
