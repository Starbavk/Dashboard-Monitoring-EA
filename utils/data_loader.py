import pandas as pd

REQUIRED_COLUMNS = [
    "Nama Kantor",
    "Nama Lengkap",
    "Pegawai V",
    "Pegawai X",
]

COLUMN_ALIASES = {
    "kantor": "Nama Kantor",
    "eselon": "Nama Kantor",
    "eselon 2": "Nama Kantor",
    "eselon ii": "Nama Kantor",
    "nama kantor": "Nama Kantor",
    "nama": "Nama Lengkap",
    "nama lengkap": "Nama Lengkap",
    "pegawai v": "Pegawai V",
    "Σ pegawai ✔": "Pegawai V",
    "pegawai x": "Pegawai X",
    "Σ pegawai ✘": "Pegawai X",
    "v": "Pegawai V",
    "x": "Pegawai X",
}

COLUMN_INDEX_MAP = {
    "Nama Kantor": 1,
    "Eselon 3": 2,
    "Nama Lengkap": 5,
    "Pegawai V": 8,
    "Pegawai X": 9,
}


def _is_ds_format(file) -> bool:
    first_row = pd.read_excel(file, engine="openpyxl", header=None, nrows=1)
    val = str(first_row.iloc[0, 0])
    return "Applied filters" in val


def _load_ds_format(file) -> pd.DataFrame:
    df_raw = pd.read_excel(file, engine="openpyxl", header=None)
    df_data = df_raw.iloc[3:].copy()
    df_data.columns = df_raw.iloc[2]
    df_data = df_data.reset_index(drop=True)

    df_out = pd.DataFrame()
    df_out["Nama Kantor"] = df_data.iloc[:, COLUMN_INDEX_MAP["Nama Kantor"]]
    df_out["Eselon 3"] = df_data.iloc[:, COLUMN_INDEX_MAP["Eselon 3"]]
    df_out["Nama Lengkap"] = df_data.iloc[:, COLUMN_INDEX_MAP["Nama Lengkap"]]

    v_col = df_data.iloc[:, COLUMN_INDEX_MAP["Pegawai V"]]
    x_col = df_data.iloc[:, COLUMN_INDEX_MAP["Pegawai X"]]

    df_out["Pegawai V"] = v_col.apply(lambda x: "Sudah" if pd.notna(x) and x == 1 else "Belum")
    df_out["Pegawai X"] = x_col.apply(lambda x: "Sudah" if pd.notna(x) and x == 1 else "Belum")

    df_out = df_out.dropna(subset=["Nama Lengkap"])
    return df_out


def _load_standard_format(file) -> pd.DataFrame:
    df = pd.read_excel(file, engine="openpyxl")
    df = _normalize_columns(df)
    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(
            f"Kolom wajib tidak ditemukan: {', '.join(missing)}. "
            f"Pastikan file memiliki kolom: {', '.join(REQUIRED_COLUMNS)}"
        )
    df["Pegawai V"] = df["Pegawai V"].apply(_normalize_status)
    df["Pegawai X"] = df["Pegawai X"].apply(_normalize_status)
    df = df.dropna(subset=["Nama Lengkap"])
    return df


def _normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df_renamed = df.rename(columns=str.strip)
    mapping = {}
    for col in df_renamed.columns:
        lower = col.lower().strip()
        if lower in COLUMN_ALIASES:
            mapping[col] = COLUMN_ALIASES[lower]
    df_renamed = df_renamed.rename(columns=mapping)
    return df_renamed


def _normalize_status(value) -> str:
    if isinstance(value, str):
        v = value.strip().lower()
        if v in ("sudah", "ya", "yes", "1", "aktif", "true"):
            return "Sudah"
        if v in ("belum", "tidak", "no", "0", "nonaktif", "false"):
            return "Belum"
    return str(value)


def load_excel(file) -> pd.DataFrame:
    if _is_ds_format(file):
        return _load_ds_format(file)
    return _load_standard_format(file)


def get_summary(df: pd.DataFrame) -> dict:
    total = len(df)
    aktif = int((df["Pegawai V"] == "Sudah").sum())
    belum = int((df["Pegawai X"] == "Sudah").sum())
    return {
        "total": total,
        "aktif": aktif,
        "belum": belum,
    }
