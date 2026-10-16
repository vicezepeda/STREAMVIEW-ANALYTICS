"""Resumen reproducible con las mismas reglas de ambos dashboards."""
import json
from pathlib import Path
import numpy as np
from prep import load_clean
import metrics as M

def resumen():
    df=load_clean()
    values={"catalogo":M.kpis_catalogo(df),"finanzas":M.kpis_financieros(df)}
    values['catalogo']['calificacion_media']=df.calificacion.mean()
    values['catalogo']['popularidad_media']=df.popularidad.mean()
    return values

if __name__=='__main__':
    values=resumen()
    text=json.dumps(values,ensure_ascii=False,indent=2,default=lambda value:value.item() if isinstance(value,np.generic) else value)
    out=Path(__file__).resolve().parents[1]/'data/processed/resumen_indicadores.json'
    out.write_text(text,encoding='utf-8')
    print(text)
