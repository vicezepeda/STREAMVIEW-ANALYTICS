"""Resultados reproducibles para responder las cuatro preguntas de negocio."""
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.prep import load_clean, explode
from src.metrics import rated_catalog, paises_calificacion

def resultados(df):
    eligible=rated_catalog(df, sufficient=True)
    genres=explode(eligible,'genres').groupby('genres').agg(
        titulos=('show_id','size'),calificacion=('calificacion','mean')).reset_index()
    genres=genres[genres.titulos>=100].sort_values('calificacion',ascending=False)
    correlations=[]
    for tipo,g in eligible.groupby('tipo'):
        correlations.append({'tipo':tipo,'n':len(g),
            'pearson':float(g.popularidad.corr(g.calificacion)),
            'spearman':float(g.popularidad.rank().corr(g.calificacion.rank()))})
    names=['Insidious','Get Out','Whiplash','Moonlight']
    f=df[df.tiene_finanzas & df.presupuesto.le(10_000_000) & df.roi_pct.gt(0) & df.titulo.isin(names)]
    return {'generos_con_evidencia':genres.to_dict('records'),
            'paises_con_evidencia':paises_calificacion(df).to_dict('records'),
            'bajo_presupuesto_ejemplos':f[['titulo','presupuesto','ingresos','roi_pct']].to_dict('records'),
            'correlacion_por_tipo':correlations}

if __name__=='__main__':
    values=resultados(load_clean())
    out=Path(__file__).resolve().parents[1]/'data/processed/respuestas_negocio.json'
    out.write_text(json.dumps(values,ensure_ascii=False,indent=2),encoding='utf-8')
    print(out.name)
