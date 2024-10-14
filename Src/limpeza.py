from pymongo import MongoClient
import pandas as pd
import numpy as np

# Conexão com o MongoDB
string_conexao = "mongodb+srv://aignosi:SuperSecret!@desafioengdados.mongocluster.cosmos.azure.com/?tls=true&authMechanism=SCRAM-SHA-256&retrywrites=false&maxIdleTimeMS=120000"
client = MongoClient(string_conexao)

# Armazenando a Base de Dados
db = client["MiningProcess"]

# Função para identificar outliers usando IQR
def identify_outliers_iqr(df, column):
    Q1 = df[column].quantile(0.25)  # Primeiro quartil (25%)
    Q3 = df[column].quantile(0.75)  # Terceiro quartil (75%)
    IQR = Q3 - Q1  # Intervalo interquartil

    # Limites para identificar outliers
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    # Identificando outliers
    outliers = df[(df[column] < lower_bound) | (df[column] > upper_bound)]
    return outliers

# Criando os DataFrames
collections = ['airflow', 'levels', 'laboratory', 'processvariables']
dfs = {}

for collection_name in collections:
    collection = db[collection_name]
    data = list(collection.find())
    df = pd.DataFrame(data)
    dfs[collection_name] = df

# Verificação de valores nulos e documentos duplicados em todas as collections
for collection_name, df in dfs.items():
    print(f"\nAnálise da coleção '{collection_name}':")
    
    # Identificando valores nulos
    print(f"Valores nulos em '{collection_name}':")
    print(df.isnull().sum())
    
    # Identificando documentos duplicados
    print(f"\nDocumentos duplicados em '{collection_name}':")
    print(df.duplicated().sum())

# Identificação de outliers usando o método IQR para todas as collections
for collection_name, df in dfs.items():
    print(f"\nOutliers na coleção '{collection_name}':")
    
    # Verificar apenas colunas numéricas
    numeric_cols = df.select_dtypes(include=np.number).columns
    for col in numeric_cols:
        outliers = identify_outliers_iqr(df, col)
        if not outliers.empty:
            print(f"\nColuna: {col}")
            print(outliers)
        else:
            print(f"\nColuna: {col} - Nenhum outlier encontrado")
