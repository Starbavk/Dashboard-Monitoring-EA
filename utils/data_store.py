import pandas as pd
import json
from pathlib import Path
from typing import Optional

DATA_PATH = Path(__file__).resolve().parent.parent / "data_store.parquet"
EDISI_PATH = Path(__file__).resolve().parent.parent / "data_edisi.json"

def save(df: pd.DataFrame):
    df.to_parquet(DATA_PATH, index=False)

def load() -> Optional[pd.DataFrame]:
    if DATA_PATH.exists():
        return pd.read_parquet(DATA_PATH)
    return None

def save_edisi(text: str):
    with open(EDISI_PATH, "w") as f:
        json.dump({"edisi": text}, f)

def load_edisi() -> str:
    if EDISI_PATH.exists():
        with open(EDISI_PATH) as f:
            return json.load(f).get("edisi", "")
    return ""
