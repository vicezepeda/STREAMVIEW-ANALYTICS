import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# ============================================================
# STREAMVIEW ANALYTICS - STORYTELLING
# Modelo narrativo AIDA
# ============================================================

# Rutas
DATA_PATH = Path("data/processed")
OUTPUT_PATH = Path("visualizaciones")
OUTPUT_PATH.mkdir(parents=True, exist_ok=True)

# ------------------------------------------------------------
# 1. CARGAR DATOS
# ------------------------------------------------------------

movies = pd.read_csv(DATA_PATH / "movies_clean.csv")
tv = pd.read_csv(DATA_PATH / "tv_shows_clean.csv")

# ============================================================
# A - ATENCIÓN
# ============================================================

total_movies = len(movies)
total_tv = len(tv)
total_catalogo = total_movies + total_tv

print("\n" + "=" * 60)
print("A - ATENCIÓN")
print("=" * 60)

print(f"StreamView posee {total_catalogo:,} títulos analizados.")
print(f"Películas: {total_movies:,}")
print(f"Series: {total_tv:,}")

# Gráfico 1: tamaño del catálogo
plt.figure(figsize=(8, 5))

plt.bar(
    ["Películas", "Series"],
    [total_movies, total_tv]
)

plt.title("StreamView: composición del catálogo")
plt.ylabel("Cantidad de títulos")

plt.tight_layout()
plt.savefig(
    OUTPUT_PATH / "story_01_catalogo.png",
    dpi=300
)

plt.close()

# ============================================================
# I - INTERÉS
# ============================================================

print("\n" + "=" * 60)
print("I - INTERÉS")
print("=" * 60)

# Promedio de rating
rating_movies = movies["vote_average"].mean()
rating_tv = tv["vote_average"].mean()

# Promedio de votos
votes_movies = movies["vote_count"].mean()
votes_tv = tv["vote_count"].mean()

print(f"Rating promedio películas: {rating_movies:.2f}/10")
print(f"Rating promedio series: {rating_tv:.2f}/10")

print(f"Votos promedio películas: {votes_movies:.0f}")
print(f"Votos promedio series: {votes_tv:.0f}")

# Gráfico 2: Rating
plt.figure(figsize=(8, 5))

plt.bar(
    ["Películas", "Series"],
    [rating_movies, rating_tv]
)

plt.title("Calificación promedio del contenido")
plt.ylabel("Rating promedio")

plt.tight_layout()
plt.savefig(
    OUTPUT_PATH / "story_02_rating.png",
    dpi=300
)

plt.close()

# Gráfico 3: interacción observable
plt.figure(figsize=(8, 5))

plt.bar(
    ["Películas", "Series"],
    [votes_movies, votes_tv]
)

plt.title("Interacción observable mediante cantidad de votos")
plt.ylabel("Promedio de votos")

plt.tight_layout()
plt.savefig(
    OUTPUT_PATH / "story_03_interaccion.png",
    dpi=300
)

plt.close()

# ============================================================
# D - DESEO
# ============================================================

print("\n" + "=" * 60)
print("D - DESEO")
print("=" * 60)

# Datos financieros
budget_available = movies["budget"].notna().sum()
revenue_available = movies["revenue"].notna().sum()

print(
    f"Películas con presupuesto disponible: "
    f"{budget_available:,} ({budget_available / total_movies * 100:.1f}%)"
)

print(
    f"Películas con ingresos disponibles: "
    f"{revenue_available:,} ({revenue_available / total_movies * 100:.1f}%)"
)

# Filtrar datos financieros válidos
financial = movies[
    (movies["budget"] > 0) &
    (movies["revenue"] > 0)
].copy()

if len(financial) > 0:

    avg_budget = financial["budget"].mean()
    avg_revenue = financial["revenue"].mean()

    print(f"Presupuesto promedio: ${avg_budget:,.0f}")
    print(f"Ingresos promedio: ${avg_revenue:,.0f}")

    # Gráfico 4: presupuesto vs ingresos
    plt.figure(figsize=(9, 6))

    plt.scatter(
        financial["budget"],
        financial["revenue"],
        alpha=0.5
    )

    plt.title("Relación entre presupuesto e ingresos")
    plt.xlabel("Presupuesto")
    plt.ylabel("Ingresos")

    plt.tight_layout()
    plt.savefig(
        OUTPUT_PATH / "story_04_finanzas.png",
        dpi=300
    )

    plt.close()

# ============================================================
# A - ACCIÓN
# ============================================================

print("\n" + "=" * 60)
print("A - ACCIÓN")
print("=" * 60)

print("""
RECOMENDACIONES PARA STREAMVIEW

1. Mejorar la calidad y disponibilidad de los datos financieros.

2. Implementar KPIs que permitan monitorear:
   - Rating promedio
   - Cantidad de votos
   - Evolución del catálogo
   - Presupuesto
   - Ingresos

3. Utilizar un dashboard interactivo para facilitar
   la toma de decisiones.

4. Analizar la concentración de géneros y mercados
   para detectar oportunidades de contenido.

5. Incorporar progresivamente datos de usuarios,
   reproducciones y suscripciones para analizar
   retención y comportamiento.
""")

# ============================================================
# RESUMEN EJECUTIVO
# ============================================================

print("\n" + "=" * 60)
print("STORYTELLING EJECUTIVO")
print("=" * 60)

print(f"""
ATENCIÓN:
StreamView cuenta con {total_catalogo:,} títulos analizados,
por lo que necesita transformar grandes volúmenes de datos
en decisiones concretas.

INTERÉS:
Las películas presentan un rating promedio de
{rating_movies:.2f}/10, mientras que las series alcanzan
{rating_tv:.2f}/10.

Además, las películas registran aproximadamente
{votes_movies:.0f} votos promedio frente a
{votes_tv:.0f} en series.

DESEO:
Los datos financieros muestran una oportunidad para
evaluar el desempeño económico del contenido, pero
la información financiera no está disponible para
todo el catálogo.

ACCIÓN:
Se recomienda consolidar los datos, implementar KPIs
y utilizar un dashboard interactivo para apoyar las
decisiones de contenido.

Conclusión:
NO SE TRATA DE TENER MÁS CONTENIDO.
SE TRATA DE INVERTIR MEJOR.
""")

print("\nStorytelling generado correctamente.")
