"""Limpieza y normalización del catálogo StreamView Analytics.

Decisiones documentadas (ver informe, sección 5 y anexo):
- Clave única = tipo + show_id (show_id se repite entre películas y series).
- budget/revenue = 0 se interpreta como dato faltante, no como valor real.
- Las series no tienen presupuesto ni ingresos (según el caso).
- Las valoraciones con pocos votos se excluyen de los rankings (umbral por tipo).
- country, genres, cast y director son multivalor: se explotan solo al analizar por categoría.
"""
import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
PROC = ROOT / "data" / "processed"
UMBRAL_MONTO = 1000  # USD; montos menores se tratan como faltantes
VOTE_MIN = {"Película": 50, "Serie": 30}  # umbral de votos para rankings de valoración


def load_raw():
    import zipfile
    names = ["netflix_movies_detailed_up_to_2025.csv", "netflix_tv_shows_detailed_up_to_2025.csv"]
    if all((RAW / name).exists() for name in names):
        return tuple(pd.read_csv(RAW / name) for name in names)
    archive = RAW / "Data_Movies.zip"
    with zipfile.ZipFile(archive) as z:
        frames = []
        for name in names:
            match = next(n for n in z.namelist() if Path(n).name == name)
            with z.open(match) as stream:
                frames.append(pd.read_csv(stream))
        return tuple(frames)


def clean(m, t):
    log = {"filas_raw_peliculas": len(m), "filas_raw_series": len(t)}
    log["show_id_compartidos_entre_tipos"] = int(len(set(m.show_id) & set(t.show_id)))

    df = pd.concat([m, t], ignore_index=True)
    df['show_id'] = df['show_id'].astype(str)
    df["tipo"] = df["type"].map({"Movie": "Película", "TV Show": "Serie"})
    dup = df.duplicated(subset=["tipo", "show_id"], keep="first")
    log["duplicados_tipo_showid_eliminados"] = int(dup.sum())
    df = df[~dup].copy()

    for c in ["country", "genres", "director", "cast"]:
        df[c] = df[c].fillna("Sin dato").astype(str).str.strip()
    df["anio"] = df["release_year"].astype(int)
    df["anio_incorporacion"] = pd.to_datetime(df["date_added"]).dt.year
    df["calificacion"] = df["vote_average"]
    df["votos"] = df["vote_count"]
    df["popularidad"] = df["popularity"]
    df["idioma"] = df["language"]
    # budget y revenue solo existen en películas; en series quedan vacíos.
    # Valores < USD 1.000 se consideran errores de registro (ej. presupuesto de USD 5) y se excluyen.
    df["presupuesto"] = df["budget"].where(df["budget"] >= UMBRAL_MONTO) if "budget" in df else pd.NA
    df["ingresos"] = df["revenue"].where(df["revenue"] >= UMBRAL_MONTO) if "revenue" in df else pd.NA
    df["tiene_finanzas"] = df["presupuesto"].notna() & df["ingresos"].notna()
    df["roi_pct"] = (df["ingresos"] - df["presupuesto"]) / df["presupuesto"] * 100
    df["votos_suficientes"] = df["votos"] >= df["tipo"].map(VOTE_MIN)

    keep = ["tipo", "show_id", "title", "anio", "anio_incorporacion", "director", "cast",
            "country", "genres", "idioma", "calificacion", "votos", "popularidad",
            "presupuesto", "ingresos", "tiene_finanzas", "roi_pct", "votos_suficientes"]
    df = df[keep].rename(columns={"title": "titulo"}).reset_index(drop=True)

    pel = df[df.tipo == "Película"]
    log["filas_limpias"] = len(df)
    log["peliculas"] = len(pel)
    log["series"] = int((df.tipo == "Serie").sum())
    log["peliculas_presupuesto_disponible"] = int(pel.presupuesto.notna().sum())
    log["peliculas_ingresos_disponibles"] = int(pel.ingresos.notna().sum())
    log["peliculas_con_ambos_datos"] = int(pel.tiene_finanzas.sum())
    log["montos_menores_a_1000_usd_excluidos"] = int(((m["budget"] > 0) & (m["budget"] < UMBRAL_MONTO)).sum()
                                                    + ((m["revenue"] > 0) & (m["revenue"] < UMBRAL_MONTO)).sum())
    log["series_con_votos_suficientes"] = int(((df.tipo == "Serie") & df.votos_suficientes).sum())
    log["peliculas_con_votos_suficientes"] = int(((df.tipo == "Película") & df.votos_suficientes).sum())
    log["duracion_disponible"] = "No: peliculas vacia, series con valor constante '1 Seasons'"
    log["clasificacion_etaria_disponible"] = False
    log["anios_por_tipo_con_1000_titulos_exactos"] = bool(
        (df.groupby(["tipo", "anio"]).size() == 1000).all())
    return df, log


def explode(df, col, sep=","):
    """Desdobla una columna multivalor en filas (excluye 'Sin dato')."""
    out = df.assign(**{col: df[col].str.split(sep)}).explode(col)
    out[col] = out[col].str.strip()
    return out[out[col].notna() & (out[col] != "") & (out[col] != "Sin dato")].drop_duplicates(["tipo", "show_id", col])


def load_clean():
    """Carga el catálogo limpio ya procesado (o lo genera si no existe)."""
    path = PROC / "catalogo_limpio.csv"
    if not path.exists():
        main()
    return pd.read_csv(path, dtype={"show_id": str})


def main():
    PROC.mkdir(parents=True, exist_ok=True)
    m, t = load_raw()
    df, log = clean(m, t)
    df.to_csv(PROC / "catalogo_limpio.csv", index=False)
    (PROC / "calidad.json").write_text(json.dumps(log, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(log, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
