import pandas as pd
import os


MOVIES_FILE = "data/processed/movies_clean.csv"
TV_FILE = "data/processed/tv_shows_clean.csv"


def load_data():

    movies = pd.read_csv(MOVIES_FILE)
    tv_shows = pd.read_csv(TV_FILE)

    return movies, tv_shows


# ============================================================
# RESUMEN GENERAL
# ============================================================

def resumen_catalogo(movies, tv_shows):

    print("\n==============================")
    print("RESUMEN DEL CATÁLOGO")
    print("==============================")

    print(f"Películas: {len(movies):,}")
    print(f"Series: {len(tv_shows):,}")

    total = len(movies) + len(tv_shows)

    print(f"Total de títulos: {total:,}")

    print(
        f"Promedio rating películas: "
        f"{movies['vote_average'].mean():.2f}"
    )

    print(
        f"Promedio rating series: "
        f"{tv_shows['vote_average'].mean():.2f}"
    )

    print(
        f"Promedio votos películas: "
        f"{movies['vote_count'].mean():.0f}"
    )

    print(
        f"Promedio votos series: "
        f"{tv_shows['vote_count'].mean():.0f}"
    )


# ============================================================
# ANÁLISIS TEMPORAL
# ============================================================

def analisis_temporal(movies, tv_shows):

    print("\n==============================")
    print("EVOLUCIÓN TEMPORAL")
    print("==============================")

    movies_year = (
        movies
        .groupby("release_year")
        .size()
        .reset_index(name="movies")
    )

    tv_year = (
        tv_shows
        .groupby("release_year")
        .size()
        .reset_index(name="tv_shows")
    )

    temporal = pd.merge(
        movies_year,
        tv_year,
        on="release_year",
        how="outer"
    ).fillna(0)

    temporal["total"] = (
        temporal["movies"] +
        temporal["tv_shows"]
    )

    temporal = temporal.sort_values("release_year")

    os.makedirs("visualizaciones", exist_ok=True)

    temporal.to_csv(
        "visualizaciones/evolucion_temporal.csv",
        index=False
    )

    print(temporal.tail(10))


# ============================================================
# ANÁLISIS DE GÉNEROS
# ============================================================

def analizar_generos(movies, tv_shows):

    print("\n==============================")
    print("GÉNEROS")
    print("==============================")

    movies_genres = (
        movies["genres"]
        .dropna()
        .str.split(", ")
        .explode()
        .value_counts()
    )

    tv_genres = (
        tv_shows["genres"]
        .dropna()
        .str.split(", ")
        .explode()
        .value_counts()
    )

    print("\nPelículas:")
    print(movies_genres.head(10))

    print("\nSeries:")
    print(tv_genres.head(10))

    movies_genres.to_csv(
        "visualizaciones/generos_peliculas.csv"
    )

    tv_genres.to_csv(
        "visualizaciones/generos_series.csv"
    )


# ============================================================
# ANÁLISIS DE IDIOMAS
# ============================================================

def analizar_idiomas(movies, tv_shows):

    print("\n==============================")
    print("IDIOMAS")
    print("==============================")

    movies_languages = (
        movies["language"]
        .dropna()
        .value_counts()
    )

    tv_languages = (
        tv_shows["language"]
        .dropna()
        .value_counts()
    )

    print("\nPelículas:")
    print(movies_languages.head(15))

    print("\nSeries:")
    print(tv_languages.head(15))

    movies_languages.to_csv(
        "visualizaciones/idiomas_peliculas.csv"
    )

    tv_languages.to_csv(
        "visualizaciones/idiomas_series.csv"
    )


# ============================================================
# ANÁLISIS FINANCIERO
# ============================================================

def analisis_financiero(movies):

    print("\n==============================")
    print("ANÁLISIS FINANCIERO")
    print("==============================")

    financial = movies[
        movies["budget"].notna() &
        movies["revenue"].notna()
    ].copy()

    print(
        f"Películas con presupuesto: "
        f"{movies['budget'].notna().sum():,}"
    )

    print(
        f"Películas con ingresos: "
        f"{movies['revenue'].notna().sum():,}"
    )

    print(
        f"Películas con ambos datos: "
        f"{len(financial):,}"
    )

    if len(financial) > 0:

        avg_budget = financial["budget"].mean()
        avg_revenue = financial["revenue"].mean()

        print(
            f"Presupuesto promedio: "
            f"${avg_budget:,.0f}"
        )

        print(
            f"Ingresos promedio: "
            f"${avg_revenue:,.0f}"
        )

        print(
            f"ROI promedio: "
            f"{financial['roi'].mean():.2f}%"
        )


# ============================================================
# EJECUCIÓN
# ============================================================

if __name__ == "__main__":

    movies, tv_shows = load_data()

    resumen_catalogo(movies, tv_shows)

    analisis_temporal(movies, tv_shows)

    analizar_generos(movies, tv_shows)

    analizar_idiomas(movies, tv_shows)

    analisis_financiero(movies)

    print("\n================================")
    print("ANÁLISIS COMPLETADO")
    print("================================")
