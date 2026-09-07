import pandas as pd
import os


# ============================================================
# CONFIGURACIÓN
# ============================================================

MOVIES_FILE = "data/raw/netflix_movies_detailed_up_to_2025.csv"
TV_FILE = "data/raw/netflix_tv_shows_detailed_up_to_2025.csv"

MOVIES_OUTPUT = "data/processed/movies_clean.csv"
TV_OUTPUT = "data/processed/tv_shows_clean.csv"


# ============================================================
# CREAR CARPETAS
# ============================================================

os.makedirs("data/processed", exist_ok=True)


# ============================================================
# FUNCIÓN PARA LIMPIAR TEXTO
# ============================================================

def clean_text(value):
    if pd.isna(value):
        return value

    return str(value).strip()


# ============================================================
# LIMPIEZA DE PELÍCULAS
# ============================================================

def clean_movies():

    print("Cargando dataset de películas...")

    df = pd.read_csv(MOVIES_FILE)

    print(f"Registros iniciales: {len(df)}")

    # Normalizar nombres de columnas
    df.columns = df.columns.str.lower().str.strip()

    # Eliminar duplicados por show_id
    df = df.drop_duplicates(subset="show_id")

    # Limpiar columnas de texto
    text_columns = [
        "title",
        "director",
        "cast",
        "country",
        "genres",
        "language",
        "description"
    ]

    for column in text_columns:
        if column in df.columns:
            df[column] = df[column].apply(clean_text)

    # Convertir fecha
    if "date_added" in df.columns:
        df["date_added"] = pd.to_datetime(
            df["date_added"],
            errors="coerce"
        )

    # Convertir variables numéricas
    numeric_columns = [
        "release_year",
        "popularity",
        "vote_count",
        "vote_average",
        "budget",
        "revenue"
    ]

    for column in numeric_columns:
        if column in df.columns:
            df[column] = pd.to_numeric(
                df[column],
                errors="coerce"
            )

    # --------------------------------------------------------
    # VALIDACIONES
    # --------------------------------------------------------

    df = df[
        (df["vote_average"].isna()) |
        ((df["vote_average"] >= 0) &
         (df["vote_average"] <= 10))
    ]

    df = df[
        (df["vote_count"].isna()) |
        (df["vote_count"] >= 0)
    ]

    df = df[
        (df["budget"].isna()) |
        (df["budget"] > 0)
    ]

    df = df[
        (df["revenue"].isna()) |
        (df["revenue"] > 0)
    ]

    # --------------------------------------------------------
    # KPI: ROI
    # --------------------------------------------------------

    df["roi"] = None

    mask = (
        df["budget"].notna() &
        df["revenue"].notna() &
        (df["budget"] > 0)
    )

    df.loc[mask, "roi"] = (
        (df.loc[mask, "revenue"] -
         df.loc[mask, "budget"])
        / df.loc[mask, "budget"]
    ) * 100

    # Guardar
    df.to_csv(
        MOVIES_OUTPUT,
        index=False,
        encoding="utf-8"
    )

    print(f"Películas procesadas: {len(df)}")
    print(f"Archivo guardado: {MOVIES_OUTPUT}")

    return df


# ============================================================
# LIMPIEZA DE SERIES
# ============================================================

def clean_tv_shows():

    print("\nCargando dataset de series...")

    df = pd.read_csv(TV_FILE)

    print(f"Registros iniciales: {len(df)}")

    # Normalizar nombres
    df.columns = df.columns.str.lower().str.strip()

    # Eliminar duplicados
    df = df.drop_duplicates(subset="show_id")

    # Limpiar texto
    text_columns = [
        "title",
        "director",
        "cast",
        "country",
        "genres",
        "language",
        "description",
        "duration"
    ]

    for column in text_columns:
        if column in df.columns:
            df[column] = df[column].apply(clean_text)

    # Convertir fechas
    if "date_added" in df.columns:
        df["date_added"] = pd.to_datetime(
            df["date_added"],
            errors="coerce"
        )

    # Variables numéricas
    numeric_columns = [
        "release_year",
        "popularity",
        "vote_count",
        "vote_average"
    ]

    for column in numeric_columns:
        if column in df.columns:
            df[column] = pd.to_numeric(
                df[column],
                errors="coerce"
            )

    # Validar rating
    df = df[
        (df["vote_average"].isna()) |
        ((df["vote_average"] >= 0) &
         (df["vote_average"] <= 10))
    ]

    # Validar votos
    df = df[
        (df["vote_count"].isna()) |
        (df["vote_count"] >= 0)
    ]

    # Guardar
    df.to_csv(
        TV_OUTPUT,
        index=False,
        encoding="utf-8"
    )

    print(f"Series procesadas: {len(df)}")
    print(f"Archivo guardado: {TV_OUTPUT}")

    return df


# ============================================================
# EJECUCIÓN
# ============================================================

if __name__ == "__main__":

    movies = clean_movies()
    tv_shows = clean_tv_shows()

    print("\n================================")
    print("PROCESAMIENTO COMPLETADO")
    print("================================")
