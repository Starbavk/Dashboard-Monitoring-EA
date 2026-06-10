import pandas as pd
from pathlib import Path
from typing import Optional

DATA_PATH = Path(__file__).resolve().parent.parent / "data_store.parquet"

def save(df: pd.DataFrame):
    df.to_parquet(DATA_PATH, index=False)

def load() -> Optional[pd.DataFrame]:
    if DATA_PATH.exists():
        return pd.read_parquet(DATA_PATH)
    return None

def exists() -> bool:
    return DATA_PATH.exists()
