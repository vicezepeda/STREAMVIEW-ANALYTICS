"""Figura estática y tabla de géneros con poblaciones separadas."""
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from src.prep import load_clean
from src.respuestas_negocio import generos_por_tipo
from src.design import PALETTE

def generate():
    root=Path(__file__).resolve().parents[1];out=root/'images';out.mkdir(exist_ok=True)
    d=generos_por_tipo(load_clean());names=['Animation','Documentary','Drama','Comedy']
    fig,axes=plt.subplots(1,2,figsize=(10.5,4.2),sharex=True,sharey=True)
    for ax,tipo in zip(axes,['Película','Serie']):
        rows=d[d.tipo.eq(tipo)].set_index('genero').loc[names].iloc[::-1]
        ax.barh(rows.index,rows.calificacion,color=PALETTE[tipo])
        for i,(_,v) in enumerate(rows.iterrows()):
            label=f'{v.calificacion:.2f} (n={int(v.titulos):,})'.replace(',','X').replace('.',',').replace('X','.')
            ax.text(v.calificacion+.12,i,label,va='center',fontsize=9)
        ax.set_title(tipo+'s' if tipo=='Serie' else 'Películas',loc='left',fontweight='bold')
        ax.set_xlim(0,10);ax.set_xlabel('Calificación media (0 a 10)')
        ax.spines[['right','top']].set_visible(False)
    fig.suptitle('Géneros por tipo: comparar adquisiciones por separado',fontsize=13,fontweight='bold')
    fig.text(.05,.01,'Nota válida. Películas >= 50 votos; series >= 30 votos. Mínimo 100 títulos por género. Categorías no exclusivas.',fontsize=8)
    fig.tight_layout(rect=(0,.05,1,.94));fig.savefig(out/'f9_generos_por_tipo.png',dpi=170);plt.close(fig)
    return d

if __name__=='__main__':generate();print('Figura f9 exportada.')
