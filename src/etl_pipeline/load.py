import logging

from sqlalchemy import text
from sqlalchemy.engine import Engine

logger = logging.getLogger(__name__)

def load_data(df, db_engine: Engine) -> None:
    logger.info(f"Upserting {len(df)} rows into PostgreSQL")

    records = df.to_dict(orient="records")

    upsert_query = text(
        """
        INSERT INTO eurostat_nasa_nf_tr (id, freq, sector, na_item, geo, unit, time, value, flag)
        VALUES (:id, :freq, :sector, :na_item, :geo, :unit, :time, :value, :flag)
        ON CONFLICT (id) DO UPDATE SET
            value = EXCLUDED.value,
            flag = EXCLUDED.flag,
            updated_at = CURRENT_TIMESTAMP;
        """
    )

    chunk_size = 5000
    for i in range(0, len(records), chunk_size):
      chunk = records[i : i + chunk_size]

      with db_engine.begin() as conn:
        conn.execute(upsert_query, chunk)

        conn.commit()

    logger.info("Pipeline load completed successfully")
