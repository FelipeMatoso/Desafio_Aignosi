from pymongo import MongoClient
import pandas as pd
import numpy as np

# Conexão com MongoDB
string_conexao = "mongodb+srv://aignosi:SuperSecret!@desafioengdados.mongocluster.cosmos.azure.com/?tls=true&authMechanism=SCRAM-SHA-256&retrywrites=false&maxIdleTimeMS=120000"
client = MongoClient(string_conexao)

# Armazenando a Base de Dados
db = client["MiningProcess"]

# Função para normalizar números que utilizam vírgula como separador decimal
def normalize_comma_numbers(df, column):
    try:
        # Verificar se há valores com vírgulas e substituí-las por pontos, e converter para float
        df[column] = df[column].str.replace(',', '.').astype(float)
    except Exception as e:
        print(f"Erro ao normalizar a coluna {column}: {e}")

# Função para verificar e normalizar campos de data
def normalize_dates(df, column):
    try:
        # Verificar se a coluna está no formato de string e converter para datetime
        df[column] = pd.to_datetime(df[column], errors='coerce')
    except Exception as e:
        print(f"Erro ao normalizar a data da coluna {column}: {e}")

# Função para aplicar normalização em todas as colunas relevantes
def normalize_dataframe(df, collection_name):
    # Identificar colunas numéricas que possam conter valores com vírgula como separador decimal
    for col in df.columns:
        if df[col].dtype == 'object':  # Verificar se a coluna é do tipo texto (object)
            if df[col].str.contains(',').any():  # Verificar se há vírgulas na coluna
                print(f"Normalizando coluna {col} na coleção {collection_name}")
                normalize_comma_numbers(df, col)
                
        # Verificar se a coluna pode ser uma data e normalizar
        if 'date' in col.lower():
            print(f"Normalizando coluna de data {col} na coleção {collection_name}")
            normalize_dates(df, col)

# Função para processar as collections
def process_collections():
    collections = ['airflow', 'levels', 'laboratory', 'processvariables']
    dfs = {}

    for collection_name in collections:
        collection = db[collection_name]
        data = list(collection.find())
        df = pd.DataFrame(data)

        if not df.empty:
            # Aplicar normalização
            normalize_dataframe(df, collection_name)
            dfs[collection_name] = df
        else:
            print(f"A coleção '{collection_name}' está vazia.")

    return dfs

# Processar e normalizar todas as collections
dfs_normalizados = process_collections()

# Exibir as primeiras linhas das collections normalizadas para verificar
for collection_name, df in dfs_normalizados.items():
    print(f"\nCollection '{collection_name}' após normalização:")
    print(df.head())
