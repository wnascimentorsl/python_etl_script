import logging

from sqlalchemy import text
from sqlalchemy.engine import Engine

logger = logging.getLogger(__name__)


def load_data(df, db_engine: Engine) -> None:
    logger.info("Upserting %s rows into PostgreSQL", len(df))

    records = df.to_dict(orient="records")

    upsert_query = text(
        """
        INSERT INTO eurostat_nasa_nf_tr (id, freq, sector, na_item, geo, unit, direct, time, value, flag)
        VALUES (:id, :freq, :sector, :na_item, :geo, :unit, :direct, :time, :value, :flag)
        ON CONFLICT (id) DO UPDATE SET
            value = EXCLUDED.value,
            flag = EXCLUDED.flag,
            updated_at = CURRENT_TIMESTAMP;
        """
    )

    chunk_size = 5000
    total_records = len(records)
    total_chunks = (total_records + chunk_size - 1) // chunk_size

    logger.info(
        "Starting load of %s records in %s chunks (chunk size: %s)",
        total_records,
        total_chunks,
        chunk_size,
    )

    for i in range(0, total_records, chunk_size):
        chunk = records[i:i + chunk_size]
        chunk_number = (i // chunk_size) + 1

        with db_engine.begin() as conn:
            conn.execute(upsert_query, chunk)

        logger.info(
            "Processed chunk %s/%s (%s records)",
            chunk_number,
            total_chunks,
            len(chunk),
        )

    logger.info("Completed loading %s records", total_records)