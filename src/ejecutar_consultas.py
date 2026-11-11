"""Ejecuta las consultas de sql/consultas.sql sobre data/superstore.db
y guarda los resultados en reports/resultados_sql.md

Uso (desde la carpeta del proyecto):  python src/ejecutar_consultas.py
"""

import sqlite3
from pathlib import Path

import pandas as pd

DB = Path("data/superstore.db")
SQL = Path("sql/consultas.sql")
OUT = Path("reports/resultados_sql.md")


def a_markdown(df):
    cols = list(df.columns)
    lineas = ["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
    for fila in df.itertuples(index=False):
        lineas.append("| " + " | ".join("" if pd.isna(v) else str(v) for v in fila) + " |")
    return "\n".join(lineas)


bloques = [b.strip() for b in SQL.read_text(encoding="utf-8").split(";") if "SELECT" in b.upper()]
salida = ["# Resultados de las consultas SQL\n"]

with sqlite3.connect(DB) as con:
    for bloque in bloques:
        lineas = bloque.splitlines()
        i = max(k for k, l in enumerate(lineas) if l.strip().startswith("--"))
        titulo = lineas[i].lstrip("- ").strip()
        consulta = "\n".join(lineas[i + 1:]).strip()

        df = pd.read_sql_query(consulta, con)
        print(f"\n== {titulo} ==")
        print(df.to_string(index=False))
        salida.append(f"## {titulo}\n\n```sql\n{consulta}\n```\n\n{a_markdown(df)}\n")

OUT.write_text("\n".join(salida), encoding="utf-8")
print("\nResultados guardados en", OUT)
