import pandas as pd
import matplotlib.pyplot as plt
import os


MOVIES_FILE = "data/processed/movies_clean.csv"
TV_FILE = "data/processed/tv_shows_clean.csv"

os.makedirs("visualizaciones", exist_ok=True)


# ============================================================
# CARGAR DATOS
# ============================================================

movies = pd.read_csv(MOVIES_FILE)
tv_shows = pd.read_csv(TV_FILE)


# ============================================================
# 1. PELÍCULAS VS SERIES
# ============================================================

types = ["Películas", "Series"]
values = [len(movies), len(tv_shows)]

plt.figure(figsize=(8, 5))

plt.bar(types, values)

plt.title("Cantidad de títulos por tipo")
plt.xlabel("Tipo de contenido")
plt.ylabel("Cantidad de títulos")

for i, value in enumerate(values):
    plt.text(
        i,
        value,
        f"{value:,}",
        ha="center",
        va="bottom"
    )

plt.tight_layout()

plt.savefig(
    "visualizaciones/catalogo_tipo.png",
    dpi=300
)

plt.close()


# ============================================================
# 2. RATING PROMEDIO
# ============================================================

ratings = [
    movies["vote_average"].mean(),
    tv_shows["vote_average"].mean()
]

plt.figure(figsize=(8, 5))

plt.bar(types, ratings)

plt.title("Rating promedio: películas vs series")
plt.xlabel("Tipo de contenido")
plt.ylabel("Rating promedio")

for i, value in enumerate(ratings):
    plt.text(
        i,
        value,
        f"{value:.2f}",
        ha="center",
        va="bottom"
    )

plt.ylim(0, 10)

plt.tight_layout()

plt.savefig(
    "visualizaciones/rating_tipo.png",
    dpi=300
)

plt.close()


# ============================================================
# 3. VOTOS PROMEDIO
# ============================================================

votes = [
    movies["vote_count"].mean(),
    tv_shows["vote_count"].mean()
]

plt.figure(figsize=(8, 5))

plt.bar(types, votes)

plt.title("Votaciones promedio: películas vs series")
plt.xlabel("Tipo de contenido")
plt.ylabel("Votaciones promedio")

for i, value in enumerate(votes):
    plt.text(
        i,
        value,
        f"{value:,.0f}",
        ha="center",
        va="bottom"
    )

plt.tight_layout()

plt.savefig(
    "visualizaciones/votaciones_tipo.png",
    dpi=300
)

plt.close()


# ============================================================
# 4. EVOLUCIÓN DEL CATÁLOGO
# ============================================================

movies_year = (
    movies
    .groupby("release_year")
    .size()
)

tv_year = (
    tv_shows
    .groupby("release_year")
    .size()
)

total_year = (
    movies_year
    .add(tv_year, fill_value=0)
    .sort_index()
)

plt.figure(figsize=(10, 5))

plt.plot(
    total_year.index,
    total_year.values,
    marker="o"
)

plt.title("Evolución del catálogo por año")
plt.xlabel("Año de lanzamiento")
plt.ylabel("Cantidad de títulos")

plt.grid(True, alpha=0.3)

plt.tight_layout()

plt.savefig(
    "visualizaciones/evolucion_catalogo.png",
    dpi=300
)

plt.close()


# ============================================================
# 5. TOP 10 GÉNEROS DE PELÍCULAS
# ============================================================

genres_movies = (
    movies["genres"]
    .dropna()
    .str.split(", ")
    .explode()
    .value_counts()
    .head(10)
    .sort_values()
)

plt.figure(figsize=(9, 6))

plt.barh(
    genres_movies.index,
    genres_movies.values
)

plt.title("Top 10 géneros de películas")
plt.xlabel("Cantidad de títulos")
plt.ylabel("Género")

plt.tight_layout()

plt.savefig(
    "visualizaciones/top_generos_peliculas.png",
    dpi=300
)

plt.close()


# ============================================================
# 6. TOP 10 GÉNEROS DE SERIES
# ============================================================

genres_tv = (
    tv_shows["genres"]
    .dropna()
    .str.split(", ")
    .explode()
    .value_counts()
    .head(10)
    .sort_values()
)

plt.figure(figsize=(9, 6))

plt.barh(
    genres_tv.index,
    genres_tv.values
)

plt.title("Top 10 géneros de series")
plt.xlabel("Cantidad de títulos")
plt.ylabel("Género")

plt.tight_layout()

plt.savefig(
    "visualizaciones/top_generos_series.png",
    dpi=300
)

plt.close()


# ============================================================
# 7. PRESUPUESTO VS INGRESOS
# ============================================================

financial = movies[
    movies["budget"].notna() &
    movies["revenue"].notna() &
    (movies["budget"] > 0) &
    (movies["revenue"] > 0)
]

plt.figure(figsize=(9, 6))

plt.scatter(
    financial["budget"],
    financial["revenue"],
    alpha=0.4
)

plt.title("Presupuesto vs ingresos de películas")
plt.xlabel("Presupuesto (USD)")
plt.ylabel("Ingresos (USD)")

plt.tight_layout()

plt.savefig(
    "visualizaciones/presupuesto_vs_ingresos.png",
    dpi=300
)

plt.close()


# ============================================================
# FINAL
# ============================================================

print("======================================")
print("VISUALIZACIONES GENERADAS CORRECTAMENTE")
print("======================================")
