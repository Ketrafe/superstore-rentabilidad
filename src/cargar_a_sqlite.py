"""Carga el CSV de Superstore a una base SQLite local (tabla `ventas`).

Uso:  python src/cargar_a_sqlite.py "data/raw/Sample - Superstore.csv"
"""
import sqlite3
import sys
from pathlib import Path

import pandas as pd

csv = Path(sys.argv[1] if len(sys.argv) > 1 else "data/raw/Sample - Superstore.csv")
db = Path("data/superstore.db")

df = pd.read_csv(csv, encoding="latin-1")
df.columns = (df.columns.str.strip().str.lower()
              .str.replace(r"[^a-z0-9]+", "_", regex=True).str.strip("_"))
for c in ["order_date", "ship_date"]:
    df[c] = pd.to_datetime(df[c], errors="coerce").dt.strftime("%Y-%m-%d")
df = df.drop_duplicates()

with sqlite3.connect(db) as con:
    df.to_sql("ventas", con, if_exists="replace", index=False)
print(f"{len(df)} filas cargadas en {db}")
