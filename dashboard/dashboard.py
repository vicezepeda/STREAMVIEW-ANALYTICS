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

st.set_page_config(page_title="StreamView - Ejecutivo Python", layout="wide")
PAL = {"Película": "#1f4e79", "Serie": "#f28e2b"}
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
st.sidebar.button('Limpiar filtros', on_click=reset_filters)
df = filter_catalog(df0, types=types, years=years, genres=genres)
st.caption(f'{len(df):,} títulos únicos seleccionados. Fuente: Netflix Movies y TV Shows hasta 2025. Año de estreno y año de incorporación son variables diferentes.')
if df.empty:
    st.warning('No hay títulos con los filtros seleccionados. Cambia los filtros o usa Limpiar filtros.')
    st.stop()
k = M.kpis_catalogo(df)
columns = st.columns(6)
for c,label,value in zip(columns,['Contenidos','Películas','Series','Países','Idiomas','Géneros'],[k['total'],k['peliculas'],k['series'],k['paises'],k['idiomas'],k['generos']]): c.metric(label,f'{value:,}')
a,b,c = st.columns(3)
a.metric('Popularidad mediana',f"{k['popularidad_mediana']:.2f}")
b.metric('Calificación con votos',f"{k['calificacion_media']:.2f} / 10" if k['calificacion_n'] else 'Sin valoraciones')
c.metric('Votaciones promedio',f'{df.votos.mean():.1f}')
st.caption(f"Calificación: promedio simple de {k['calificacion_n']:,} títulos con votos > 0 y nota > 0. "
           f"Se excluyen {k['calificacion_excluidos']:,} títulos sin valoración utilizable. "
           f"Popularidad: mediana {k['popularidad_mediana']:.2f}, media {k['popularidad_media']:.2f} (índice de la fuente).")
view,territory,d3tab = st.tabs(['Vista general','Países e idiomas','Exploración D3'])
with view:
    a,b = st.columns(2)
    for target,column,title in [(a,'anio','Títulos por año de estreno'),(b,'anio_incorporacion','Incorporaciones por año')]:
        temp = df.groupby([column,'tipo']).size().reset_index(name='titulos')
        line = px.line(temp,x=column,y='titulos',color='tipo',markers=True,color_discrete_map=PAL,title=title,labels={column:'Año','titulos':'Títulos','tipo':'Tipo'})
        line.update_yaxes(range=[0, max(temp.titulos.max()*1.15,1)])
        target.plotly_chart(line, width='stretch')
    st.caption('La distribución por año de estreno es casi uniforme en la fuente; no permite afirmar crecimiento real del catálogo.')
    a,b = st.columns(2)
    g = M.top_generos(df)
    a.plotly_chart(px.bar(g.iloc[::-1],x='titulos',y='genres',orientation='h',title='Top 10 géneros',labels={'genres':'Género','titulos':'Títulos'},color_discrete_sequence=['#1f4e79']),width='stretch')
    p = M.top_paises(df)
    b.plotly_chart(px.bar(p.iloc[::-1],x='titulos',y='country',orientation='h',title='Top 10 países',labels={'country':'País','titulos':'Títulos'},color_discrete_sequence=['#1f4e79']),width='stretch')
    dist = df.groupby('tipo').size().reset_index(name='titulos')
    st.plotly_chart(px.bar(dist,x='tipo',y='titulos',color='tipo',color_discrete_map=PAL,title='Películas y series',labels={'tipo':'Tipo','titulos':'Títulos'}),width='stretch')
with territory:
    p = explode(df,'country').groupby('country').size().reset_index(name='titulos')
    p['iso3'] = p.country.map(iso3)
    mapped = p[p.iso3.notna()]
    fig=px.choropleth(mapped,locations='iso3',locationmode='ISO-3',color='titulos',hover_name='country',color_continuous_scale='Blues',title='Producciones por país',labels={'titulos':'Títulos'})
    st.plotly_chart(fig,width='stretch',config=MAP_CONFIG)
    st.caption('Países y géneros son multivalor. Un título puede aparecer en más de una categoría; el total de contenidos siempre cuenta títulos únicos.')
    if p.iso3.isna().any():st.caption('Sin correspondencia geográfica: '+', '.join(p.loc[p.iso3.isna(),'country']))
    l=M.idiomas(df).melt(id_vars=['idioma','total'],var_name='tipo',value_name='titulos')
    st.plotly_chart(px.bar(l,x='idioma',y='titulos',color='tipo',barmode='group',color_discrete_map=PAL,title='Idiomas principales',labels={'idioma':'Código de idioma','titulos':'Títulos','tipo':'Tipo'}),width='stretch')
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
st.download_button('Descargar catálogo filtrado',df.to_csv(index=False).encode('utf-8'),'catalogo_filtrado.csv','text/csv')
st.info('No hay clasificación etaria utilizable en la fuente. Popularidad y votos no equivalen a reproducciones ni permiten medir retención o churn.')
