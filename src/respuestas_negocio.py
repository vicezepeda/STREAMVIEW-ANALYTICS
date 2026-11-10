"""Resultados reproducibles para responder las cuatro preguntas de negocio."""
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.prep import load_clean, explode
from src.metrics import rated_catalog, paises_calificacion

def generos_por_tipo(df, min_titulos=100):
    """Comparaciones editoriales separadas: películas >=50 votos, series >=30.

    Cada tipo conserva sus categorías de origen. La nota es media simple y
    el tamaño de muestra cuenta títulos únicos dentro de cada género.
    """
    eligible=explode(rated_catalog(df,sufficient=True),'genres')
    genres=eligible.groupby(['tipo','genres']).agg(
        titulos=('show_id','size'),calificacion=('calificacion','mean')).reset_index()
    genres=genres[genres.titulos>=min_titulos].sort_values(
        ['tipo','calificacion','genres'],ascending=[True,False,True])
    genres['umbral_votos']=genres.tipo.map({'Película':50,'Serie':30})
    return genres.rename(columns={'genres':'genero'})

def resultados(df):
    eligible=rated_catalog(df, sufficient=True)
    genres=generos_por_tipo(df)
    countries=[]
    for tipo,g in df.groupby('tipo'):
        for row in paises_calificacion(g).to_dict('records'):
            countries.append({'tipo':tipo,**row})
    correlations=[]
    for tipo,g in eligible.groupby('tipo'):
        correlations.append({'tipo':tipo,'n':len(g),
            'pearson':float(g.popularidad.corr(g.calificacion)),
            'spearman':float(g.popularidad.rank().corr(g.calificacion.rank()))})
    names=['Insidious','Get Out','Whiplash','Moonlight']
    f=df[df.tiene_finanzas & df.presupuesto.le(10_000_000) & df.roi_pct.gt(0) & df.titulo.isin(names)]
    return {'generos_por_tipo_con_evidencia':genres.to_dict('records'),
            'paises_con_evidencia':paises_calificacion(df).to_dict('records'),
            'paises_por_tipo_con_evidencia':countries,
            'bajo_presupuesto_ejemplos':f[['titulo','presupuesto','ingresos','roi_pct']].to_dict('records'),
            'correlacion_por_tipo':correlations}

if __name__=='__main__':
    values=resultados(load_clean())
    out=Path(__file__).resolve().parents[1]/'data/processed/respuestas_negocio.json'
    out.write_text(json.dumps(values,ensure_ascii=False,indent=2),encoding='utf-8')
    generos_por_tipo(load_clean()).to_csv(out.with_name('generos_por_tipo.csv'),index=False,encoding='utf-8-sig')
    print(out.name)
