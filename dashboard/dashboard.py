import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# ============================================================
# STREAMVIEW ANALYTICS - DASHBOARD
# ============================================================

st.set_page_config(
    page_title="StreamView Analytics",
    page_icon="🎬",
    layout="wide"
)

# ============================================================
# CARGA DE DATOS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "processed"

MOVIES_FILE = DATA_DIR / "movies_clean.csv"
TV_FILE = DATA_DIR / "tv_shows_clean.csv"


@st.cache_data
def load_data():

    movies = pd.read_csv(MOVIES_FILE)
    tv = pd.read_csv(TV_FILE)

    movies["tipo"] = "Película"
    tv["tipo"] = "Serie"

    return movies, tv


movies, tv = load_data()

# ============================================================
# PREPARAR DATOS
# ============================================================

movies["year"] = pd.to_numeric(
    movies["year"], errors="coerce"
)

tv["year"] = pd.to_numeric(
    tv["year"], errors="coerce"
)

# ============================================================
# TÍTULO
# ============================================================

st.title("🎬 StreamView Analytics")

st.subheader(
    "Dashboard ejecutivo para la toma de decisiones sobre contenido"
)

st.write(
    "Explora el catálogo, sus principales características, "
    "la interacción observable mediante votos y la información financiera disponible."
)

st.divider()

# ============================================================
# FILTROS
# ============================================================

st.sidebar.header("🔎 Filtros")

tipo = st.sidebar.multiselect(
    "Tipo de contenido",
    options=["Película", "Serie"],
    default=["Película", "Serie"]
)

# Unir datasets
data = pd.concat(
    [movies, tv],
    ignore_index=True
)

# Aplicar filtro tipo
data = data[data["tipo"].isin(tipo)]

# Filtro de años
min_year = int(data["year"].min())
max_year = int(data["year"].max())

years = st.sidebar.slider(
    "Rango de años",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year)
)

data = data[
    (data["year"] >= years[0]) &
    (data["year"] <= years[1])
]

# ============================================================
# KPIs
# ============================================================

total_titles = len(data)

movies_count = len(
    data[data["tipo"] == "Película"]
)

tv_count = len(
    data[data["tipo"] == "Serie"]
)

avg_rating = data["vote_average"].mean()

avg_votes = data["vote_count"].mean()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "🎬 Títulos",
        f"{total_titles:,}"
    )

with col2:
    st.metric(
        "🎞️ Películas",
        f"{movies_count:,}"
    )

with col3:
    st.metric(
        "📺 Series",
        f"{tv_count:,}"
    )

with col4:
    st.metric(
        "⭐ Rating promedio",
        f"{avg_rating:.2f}/10"
    )

st.divider()

# ============================================================
# PRIMERA FILA DE GRÁFICOS
# ============================================================

col1, col2 = st.columns(2)

# ------------------------------------------------------------
# CATÁLOGO POR TIPO
# ------------------------------------------------------------

with col1:

    st.subheader("Composición del catálogo")

    catalogo = (
        data["tipo"]
        .value_counts()
        .reset_index()
    )

    catalogo.columns = [
        "Tipo",
        "Cantidad"
    ]

    fig = px.pie(
        catalogo,
        names="Tipo",
        values="Cantidad",
        hole=0.45,
        title="Películas vs. series"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ------------------------------------------------------------
# RATING
# ------------------------------------------------------------

with col2:

    st.subheader("Rating promedio")

    rating = (
        data.groupby("tipo")["vote_average"]
        .mean()
        .reset_index()
    )

    fig = px.bar(
        rating,
        x="tipo",
        y="vote_average",
        title="Rating promedio por tipo",
        labels={
            "tipo": "Contenido",
            "vote_average": "Rating"
        },
        range_y=[0, 10]
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ============================================================
# SEGUNDA FILA
# ============================================================

col1, col2 = st.columns(2)

# ------------------------------------------------------------
# EVOLUCIÓN TEMPORAL
# ------------------------------------------------------------

with col1:

    st.subheader("Evolución del catálogo")

    evolution = (
        data.groupby(
            ["year", "tipo"]
        )
        .size()
        .reset_index(name="cantidad")
    )

    fig = px.line(
        evolution,
        x="year",
        y="cantidad",
        color="tipo",
        markers=True,
        title="Cantidad de títulos por año",
        labels={
            "year": "Año",
            "cantidad": "Títulos",
            "tipo": "Tipo"
        }
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ------------------------------------------------------------
# VOTOS
# ------------------------------------------------------------

with col2:

    st.subheader("Interacción observable")

    votes = (
        data.groupby("tipo")["vote_count"]
        .mean()
        .reset_index()
    )

    fig = px.bar(
        votes,
        x="tipo",
        y="vote_count",
        title="Promedio de votos por tipo",
        labels={
            "tipo": "Contenido",
            "vote_count": "Promedio de votos"
        }
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.divider()

# ============================================================
# GÉNEROS
# ============================================================

st.subheader("🎭 Principales géneros")

genre_data = data[
    data["genres"].notna()
].copy()

genre_data["genres"] = (
    genre_data["genres"]
    .astype(str)
    .str.split(",")
)

genre_data = genre_data.explode("genres")

genre_data["genres"] = (
    genre_data["genres"]
    .str.strip()
)

top_genres = (
    genre_data["genres"]
    .value_counts()
    .head(10)
    .reset_index()
)

top_genres.columns = [
    "Genero",
    "Cantidad"
]

fig = px.bar(
    top_genres.sort_values("Cantidad"),
    x="Cantidad",
    y="Genero",
    orientation="h",
    title="Top 10 géneros del catálogo",
    labels={
        "Cantidad": "Cantidad de títulos",
        "Genero": "Género"
    }
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

# ============================================================
# INFORMACIÓN FINANCIERA
# ============================================================

st.subheader("💰 Información financiera")

financial = data[
    (data["tipo"] == "Película") &
    (data["budget"] > 0) &
    (data["revenue"] > 0)
].copy()

if len(financial) > 0:

    col1, col2, col3 = st.columns(3)

    avg_budget = financial["budget"].mean()
    avg_revenue = financial["revenue"].mean()

    with col1:
        st.metric(
            "Presupuesto promedio",
            f"${avg_budget / 1_000_000:.1f} M"
        )

    with col2:
        st.metric(
            "Ingresos promedio",
            f"${avg_revenue / 1_000_000:.1f} M"
        )

    with col3:
        ratio = avg_revenue / avg_budget

        st.metric(
            "Ingresos / presupuesto",
            f"{ratio:.2f}x"
        )

    # Scatter
    fig = px.scatter(
        financial,
        x="budget",
        y="revenue",
        hover_data=["title", "year"],
        title="Presupuesto vs. ingresos",
        labels={
            "budget": "Presupuesto",
            "revenue": "Ingresos"
        }
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

else:

    st.warning(
        "No existen datos financieros válidos para los filtros seleccionados."
    )

st.divider()

# ============================================================
# CONCLUSIONES
# ============================================================

st.subheader("📌 Hallazgos principales")

st.markdown(
    """
### 1. Catálogo amplio
StreamView dispone de un catálogo de gran tamaño, compuesto por
películas y series.

### 2. Diferencias entre formatos
Las películas y series presentan diferencias en rating e interacción
observable mediante la cantidad de votos.

### 3. Concentración de géneros
El catálogo presenta concentración en determinados géneros, lo que
permite identificar oportunidades de diversificación.

### 4. Información financiera limitada
Los datos de presupuesto e ingresos están disponibles solamente para
una parte del catálogo de películas.

### 5. Oportunidad de mejora
La incorporación de datos de usuarios, reproducciones y suscripciones
permitiría complementar este análisis con indicadores de retención,
comportamiento y churn.
"""
)

st.success(
    "🎯 No se trata de tener más contenido. Se trata de invertir mejor."
)

# ============================================================
# PIE
# ============================================================

st.caption(
    "StreamView Analytics | Proyecto de Visualización de Datos"
  )
