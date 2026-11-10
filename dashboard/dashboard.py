"""Dashboard ejecutivo para Directorio y Gerencia General (Python)."""
import json
import sys
from pathlib import Path
import pandas as pd
import plotly.express as px
import pycountry
import streamlit as st
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.prep import load_clean, explode
from src import metrics as M
from src.filters import filter_catalog
from src.respuestas_negocio import generos_por_tipo
from src.design import PALETTE

st.set_page_config(page_title="StreamView - Ejecutivo Python", layout="wide")
PAL = PALETTE
MAP_CONFIG = {"topojsonURL": "/app/static/"}

@st.cache_data
def data(): return load_clean()

def reset_filters():
    st.session_state['tipos'] = ['Película', 'Serie']
    st.session_state['anios'] = (2010, 2025)
    st.session_state['generos'] = []

ALIASES = {'United States of America':'USA','South Korea':'KOR','North Korea':'PRK','Russia':'RUS','Vietnam':'VNM','Czech Republic':'CZE','Kosovo':'XKX','Iran':'IRN','Syria':'SYR','Laos':'LAO','Bolivia':'BOL','Venezuela':'VEN','Taiwan':'TWN','Palestine':'PSE',"Cote D'Ivoire":'CIV','Faeroe Islands':'FRO','Guadaloupe':'GLP','Macedonia':'MKD','Netherlands Antilles':'ANT','Palestinian Territory':'PSE','St. Kitts and Nevis':'KNA','St. Lucia':'LCA','St. Pierre and Miquelon':'SPM','Turkey':'TUR','US Virgin Islands':'VIR'}
def iso3(country):
    if country in ALIASES: return ALIASES[country]
    try: return pycountry.countries.lookup(country).alpha_3
    except LookupError: return None

df0 = data()
st.title('StreamView Analytics')
st.subheader('Dashboard ejecutivo en Python')
st.caption('Audiencia: Directorio y Gerencia General. La audiencia de Contenidos y Adquisición se implementa en el PBIX de la carpeta powerbi/.')
st.sidebar.header('Filtros ejecutivos')
for key, initial in {'tipos': ['Película', 'Serie'], 'anios': (2010, 2025), 'generos': []}.items():
    if key not in st.session_state:
        st.session_state[key] = initial
types = st.sidebar.multiselect('Tipo de contenido', ['Película','Serie'], key='tipos')
years = st.sidebar.slider('Rango de años de estreno',2010,2025,key='anios')
genres = st.sidebar.multiselect('Género', sorted(explode(df0,'genres').genres.unique()), key='generos')
st.sidebar.button('Limpiar filtros', on_click=reset_filters, key='limpiar')
df = filter_catalog(df0, types=types, years=years, genres=genres)
st.caption(f'{len(df):,} títulos únicos seleccionados. Fuente: Netflix Movies y TV Shows hasta 2025. Año de estreno y año de incorporación son variables diferentes.')
if df.empty:
    st.warning('No hay títulos con los filtros seleccionados. Cambia los filtros o usa Limpiar filtros.')
    st.stop()
k = M.kpis_catalogo(df)
columns = st.columns(3)
for c,label,value in zip(columns,['Contenidos','Películas','Series'],[k['total'],k['peliculas'],k['series']]): c.metric(label,f'{value:,}')
a,b,c = st.columns(3)
a.metric('Calificación con votos',f"{k['calificacion_media']:.2f} / 10" if k['calificacion_n'] else 'Sin valoraciones')
b.metric('Popularidad mediana',f"{k['popularidad_mediana']:.2f}")
c.metric('Valoraciones válidas',f"{k['calificacion_n']:,}")
with st.expander('Países, idiomas y otros indicadores'):
    columns=st.columns(4)
    for col,label,value in zip(columns,['Países','Idiomas','Géneros','Votaciones promedio'],[k['paises'],k['idiomas'],k['generos'],round(df.votos.mean(),1)]):
        col.metric(label,str(value))
st.caption(f"Calificación: promedio simple de {k['calificacion_n']:,} títulos con votos > 0 y nota > 0. "
           f"Se excluyen {k['calificacion_excluidos']:,} títulos sin valoración utilizable. "
           f"Popularidad: mediana {k['popularidad_mediana']:.2f}, media {k['popularidad_media']:.2f} (índice de la fuente).")
view,comparison,territory,d3tab = st.tabs(['Vista general','Géneros por tipo','Países e idiomas','Exploración D3'])
st.caption('Filtros activos: '+', '.join(types)+'; estreno '+str(years[0])+' a '+str(years[1])+'; géneros: '+(', '.join(genres) if genres else 'todos')+'.')

def show_chart(target,fig,**kwargs):
    fig.update_layout(template='plotly_white',font={'family':'Arial','size':16,'color':'#26384A'},height=430)
    target.plotly_chart(fig,width='stretch',**kwargs)
with view:
    a,b = st.columns(2)
    for target,column,title in [(a,'anio','Títulos por año de estreno'),(b,'anio_incorporacion','Incorporaciones por año')]:
        temp = df.groupby([column,'tipo']).size().reset_index(name='titulos')
        line = px.line(temp,x=column,y='titulos',color='tipo',line_dash='tipo',symbol='tipo',markers=True,color_discrete_map=PAL,title=title,labels={column:'Año','titulos':'Títulos','tipo':'Tipo'})
        line.update_yaxes(range=[0, max(temp.titulos.max()*1.15,1)])
        show_chart(target,line)
    st.caption('La distribución por año de estreno es casi uniforme en la fuente; no permite afirmar crecimiento real del catálogo.')
    a,b = st.columns(2)
    g = M.top_generos(df)
    show_chart(a,px.bar(g.iloc[::-1],x='titulos',y='genres',orientation='h',title='Top 10 géneros por volumen',labels={'genres':'Género','titulos':'Títulos'},color_discrete_sequence=['#1f4e79']))
    p = M.top_paises(df)
    show_chart(b,px.bar(p.iloc[::-1],x='titulos',y='country',orientation='h',title='Top 10 países',labels={'country':'País','titulos':'Títulos'},color_discrete_sequence=['#1f4e79']))
    dist = df.groupby('tipo').size().reset_index(name='titulos')
    show_chart(st,px.bar(dist,x='tipo',y='titulos',color='tipo',pattern_shape='tipo',color_discrete_map=PAL,title='Películas y series',labels={'tipo':'Tipo','titulos':'Títulos'}))
with comparison:
    st.subheader('Comparar géneros dentro de cada tipo')
    st.write('Películas y series se evalúan por separado para orientar la revisión de contenidos y sus licencias.')
    minimum=st.number_input('Mínimo de títulos por género',min_value=1,max_value=2000,value=100,step=25,key='min_genero')
    grouped=generos_por_tipo(df,min_titulos=minimum)
    st.caption('Nota > 0 y <= 10. Películas: mínimo 50 votos. Series: mínimo 30 votos. n cuenta títulos únicos dentro de cada género. Los filtros superiores también se aplican aquí.')
    if grouped.empty:
        st.info('Ningún género alcanza el mínimo con estos filtros. Reduce el mínimo o limpia los filtros.')
    else:
        for target,tipo in zip(st.columns(2),['Película','Serie']):
            g=grouped[grouped.tipo.eq(tipo)].head(7).iloc[::-1]
            if not g.empty:
                fig=px.bar(g,x='calificacion',y='genero',orientation='h',text='calificacion',title=tipo,hover_data=['titulos','umbral_votos'],labels={'genero':'Género','calificacion':'Calificación media'},color_discrete_sequence=[PAL[tipo]])
                fig.update_xaxes(range=[0,10]);fig.update_traces(texttemplate='%{text:.2f}',textposition='outside')
                show_chart(target,fig)
        display=grouped.rename(columns={'tipo':'Tipo','genero':'Género','titulos':'n títulos','calificacion':'Nota media','umbral_votos':'Mínimo de votos'}).copy()
        display['Nota media']=display['Nota media'].round(2)
        st.dataframe(display,hide_index=True,width='stretch')
        st.download_button('Descargar comparación por tipo',grouped.to_csv(index=False).encode('utf-8-sig'),'generos_por_tipo_filtrado.csv','text/csv',key='csv_generos')
    st.info('La valoración ayuda a seleccionar candidatos. La decisión de compra necesita consumo, costos y derechos de licencia. Las categorías de películas y series no se homologan automáticamente.')
with territory:
    p = explode(df,'country').groupby('country').size().reset_index(name='titulos')
    p['iso3'] = p.country.map(iso3)
    mapped = p[p.iso3.notna()]
    fig=px.choropleth(mapped,locations='iso3',locationmode='ISO-3',color='titulos',hover_name='country',color_continuous_scale='Blues',title='Producciones por país',labels={'titulos':'Títulos'})
    show_chart(st,fig,config=MAP_CONFIG)
    st.caption('Países y géneros son multivalor. Un título puede aparecer en más de una categoría; el total de contenidos siempre cuenta títulos únicos.')
    if p.iso3.isna().any():st.caption('Sin correspondencia geográfica: '+', '.join(p.loc[p.iso3.isna(),'country']))
    l=M.idiomas(df).melt(id_vars=['idioma','total'],var_name='tipo',value_name='titulos')
    show_chart(st,px.bar(l,x='idioma',y='titulos',color='tipo',pattern_shape='tipo',barmode='group',color_discrete_map=PAL,title='Idiomas principales',labels={'idioma':'Código de idioma','titulos':'Títulos','tipo':'Tipo'}))
    st.dataframe(p[['country','titulos']],hide_index=True,width='stretch')
with d3tab:
    g=explode(df,'genres').groupby('genres').size().reset_index(name='titulos').rename(columns={'genres':'genero'})
    rating_by_genre=explode(M.rated_catalog(df),'genres').groupby('genres').calificacion.mean()
    g['calificacion']=g.genero.map(rating_by_genre)
    library=(ROOT/'dashboard/d3/vendor/d3.v7.min.js').read_text(encoding='utf-8')
    template=(ROOT/'dashboard/d3/generos.html').read_text(encoding='utf-8-sig')
    payload=g.to_json(orient='records',force_ascii=False).replace('<','\\u003c')
    st.iframe(template.replace('__D3_LIBRARY__',library).replace('__DATA__',payload),
              height=530, alt='Comparación de géneros con D3')
    with st.expander('Ver los datos del gráfico D3'):
        st.dataframe(g.rename(columns={'genero':'Género','titulos':'Títulos','calificacion':'Nota media'}).round(2),hide_index=True,width='stretch')
    st.caption('La vista D3 describe el catálogo seleccionado. Para recomendar adquisiciones usa Géneros por tipo o filtra un solo tipo.')
st.download_button('Descargar catálogo filtrado',df.to_csv(index=False).encode('utf-8'),'catalogo_filtrado.csv','text/csv')
st.info('No hay clasificación etaria utilizable en la fuente. Popularidad y votos no equivalen a reproducciones ni permiten medir retención o churn.')
