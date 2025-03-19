pip install streamlit pandas requests matplotlib folium streamlit-folium

import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static

# Configuração do título do Dashboard
st.set_page_config(page_title="Saúde em Minas Gerais", layout="wide")

# Título e introdução
st.title("📊 Dashboard Comparativo de Saúde - Minas Gerais")
st.write("Este painel exibe indicadores de saúde para os 853 municípios de MG, com atualização automática via API.")

# Carregar dados
@st.cache_data
def load_data():
    try:
        df_mortalidade = pd.read_csv("data/mortalidade_materna.csv")
        df_dengue = pd.read_csv("data/dengue.csv")
        return df_mortalidade, df_dengue
    except:
        st.error("Erro ao carregar os dados.")
        return None, None

df_mortalidade, df_dengue = load_data()

# Criar um seletor de município
municipios = df_mortalidade["municipio"].unique()
municipio_selecionado = st.selectbox("Selecione um município:", municipios)

# Exibir dados do município selecionado
if municipio_selecionado:
    dados_municipio = df_mortalidade[df_mortalidade["municipio"] == municipio_selecionado]
    st.subheader(f"📍 Indicadores de Saúde - {municipio_selecionado}")

    # Exibir tabelas de dados
    st.write("### Mortalidade Materna")
    st.dataframe(dados_municipio)

    st.write("### Casos de Dengue")
    dados_dengue_municipio = df_dengue[df_dengue["municipio"] == municipio_selecionado]
    st.dataframe(dados_dengue_municipio)

# Criar mapa interativo com dados de dengue
st.write("### 🌍 Mapa de Casos de Dengue")

# Criar mapa
mapa = folium.Map(location=[-18.5122, -44.5550], zoom_start=6)

for _, row in df_dengue.iterrows():
    folium.CircleMarker(
        location=[row["latitude"], row["longitude"]],
        radius=row["casos"] / 100,  # Ajustar tamanho do círculo proporcionalmente
        color="red",
        fill=True,
        fill_color="red",
        fill_opacity=0.6,
        popup=f"{row['municipio']}: {row['casos']} casos",
    ).add_to(mapa)

# Exibir mapa no Streamlit
folium_static(mapa)

