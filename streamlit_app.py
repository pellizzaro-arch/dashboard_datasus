pip install streamlit pandas requests matplotlib folium streamlit-folium

import requests
import pandas as pd
import os

# Criar pasta para armazenar os dados
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

# Função para buscar dados de mortalidade materna
def fetch_mortalidade_materna():
    url = "https://api.datasus.saude.gov.br/mortalidade_materna?uf=MG&ano=2024"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data)
        df.to_csv(os.path.join(DATA_DIR, "mortalidade_materna.csv"), index=False)
        print("Mortalidade materna atualizada.")
    else:
        print("Erro ao acessar a API de mortalidade materna.")

# Função para buscar dados de dengue
def fetch_dados_dengue():
    url = "https://api.datasus.saude.gov.br/dengue?uf=MG&ano=2024"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data)
        df.to_csv(os.path.join(DATA_DIR, "dengue.csv"), index=False)
        print("Casos de dengue atualizados.")
    else:
        print("Erro ao acessar a API de dengue.")

# Executa a coleta de dados
if __name__ == "__main__":
    fetch_mortalidade_materna()
    fetch_dados_dengue()
