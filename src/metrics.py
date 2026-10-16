"""KPIs del catálogo. Fuente única para dashboard, figuras e informe."""
import pandas as pd

try:
    from src.prep import explode
except ImportError:  # ejecución directa desde src/
    from prep import explode

ASIA = ["ja", "ko", "zh"]


def kpis_catalogo(df: pd.DataFrame) -> dict:
    pel = df[df.tipo == "Película"]
    ser = df[df.tipo == "Serie"]
    ok = df[df.votos_suficientes]
    return {
        "total": len(df),
        "peliculas": len(pel),
        "series": len(ser),
        "paises": explode(df, "country").country.nunique(),
        "idiomas": df.idioma.nunique(),
        "generos": explode(df, "genres").genres.nunique(),
        "popularidad_mediana_peliculas": pel.popularidad.median(),
        "popularidad_mediana_series": ser.popularidad.median(),
        "calificacion_prom_ponderada": (ok.calificacion * ok.votos).sum() / ok.votos.sum() if ok.votos.sum() else float("nan"),
        "pct_en": (df.idioma == "en").mean() * 100,
        "pct_asia": df.idioma.isin(ASIA).mean() * 100,
    }


def kpis_financieros(df: pd.DataFrame) -> dict:
    """Solo películas con presupuesto e ingresos informados (pareados)."""
    f = df[df.tiene_finanzas]
    bud, rev = f.presupuesto.sum(), f.ingresos.sum()
    return {
        "n": len(f),
        "cobertura_pct": len(f) / max(len(df[df.tipo == "Película"]), 1) * 100,
        "presupuesto_prom": f.presupuesto.mean(),
        "ingresos_prom": f.ingresos.mean(),
        "presupuesto_total": bud,
        "ingresos_total": rev,
        "ratio_ingresos_presupuesto": rev / bud if bud else float("nan"),
        "roi_agregado_pct": (rev - bud) / bud * 100 if bud else float("nan"),
        "roi_mediano_pct": f.roi_pct.median(),
        "pct_recuperan_presupuesto": (f.roi_pct > 0).mean() * 100,
    }


def por_anio(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby(["anio", "tipo"]).size().unstack(fill_value=0).reset_index()


def top_paises(df: pd.DataFrame, n=10) -> pd.DataFrame:
    e = explode(df, "country")
    return e.groupby(["country", "tipo"]).size().reset_index(name="titulos") \
        .groupby("country").titulos.sum().sort_values(ascending=False).head(n).reset_index()


def top_generos(df: pd.DataFrame, n=10) -> pd.DataFrame:
    e = explode(df, "genres")
    return e.groupby(["genres", "tipo"]).size().reset_index(name="titulos") \
        .groupby("genres").titulos.sum().sort_values(ascending=False).head(n).reset_index()


def generos_resumen(df: pd.DataFrame, min_titulos=100) -> pd.DataFrame:
    e = explode(df, "genres")
    g = e.groupby("genres").agg(titulos=("titulo", "size"),
                                popularidad_mediana=("popularidad", "median"),
                                calificacion_prom=("calificacion", "mean")).reset_index()
    return g[g.titulos >= min_titulos].sort_values("titulos", ascending=False)


def top_directores(df: pd.DataFrame, n=10) -> pd.DataFrame:
    e = explode(df, "director")
    return e.groupby("director").size().sort_values(ascending=False).head(n).reset_index(name="titulos")


def top_actores(df: pd.DataFrame, n=10) -> pd.DataFrame:
    e = explode(df, "cast")
    return e.groupby("cast").size().sort_values(ascending=False).head(n).reset_index(name="titulos")


def paises_calificacion(df: pd.DataFrame, min_titulos=30) -> pd.DataFrame:
    e = explode(df[df.votos_suficientes], "country")
    g = e.groupby("country").agg(titulos=("titulo", "size"), calificacion_prom=("calificacion", "mean"),
                                 popularidad_mediana=("popularidad", "median")).reset_index()
    return g[g.titulos >= min_titulos].sort_values("calificacion_prom", ascending=False)


def top_mejor_evaluados(df: pd.DataFrame, votos_min=1000, n=10) -> pd.DataFrame:
    d = df[df.votos >= votos_min]
    return d.sort_values(["calificacion", "votos"], ascending=False).head(n)[
        ["titulo", "tipo", "calificacion", "votos", "anio"]]


def idiomas(df: pd.DataFrame, n=8) -> pd.DataFrame:
    g = df.groupby(["idioma", "tipo"]).size().unstack(fill_value=0)
    g["total"] = g.sum(axis=1)
    return g.sort_values("total", ascending=False).head(n).reset_index()
