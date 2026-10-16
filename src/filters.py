"""Filtros de catálogo con coincidencia exacta de cada categoría multivalor."""
def filter_catalog(df, types=None, years=None, genres=None, countries=None, languages=None, rating=None):
    result = df.copy()
    if types is not None:
        result = result[result.tipo.isin(types)]
    if years is not None:
        result = result[result.anio.between(*years)]
    if languages:
        result = result[result.idioma.isin(languages)]
    if rating is not None:
        result = result[result.calificacion.between(*rating)]
    for column, values in [("genres", genres), ("country", countries)]:
        if values:
            selected = set(values)
            result = result[result[column].apply(lambda text: bool(selected.intersection(part.strip() for part in str(text).split(","))))]
    return result
