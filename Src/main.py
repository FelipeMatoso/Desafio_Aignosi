from pymongo import MongoClient
import pandas as pd

# Conexão com MongoDB
string_conexao = "mongodb+srv://aignosi:SuperSecret!@desafioengdados.mongocluster.cosmos.azure.com/?tls=true&authMechanism=SCRAM-SHA-256&retrywrites=false&maxIdleTimeMS=120000"
client = MongoClient(string_conexao)
db = client["MiningProcess"]

# Função para normalizar números que utilizam vírgula como separador decimal
def normalize_comma_numbers(df, column):
    try:
        df[column] = df[column].str.replace(',', '.').astype(float)
    except Exception as e:
        print(f"Erro ao normalizar a coluna {column}: {e}")

# Função para verificar e normalizar campos de data
def normalize_dates(df, column):
    try:
        df[column] = pd.to_datetime(df[column], errors='coerce')
    except Exception as e:
        print(f"Erro ao normalizar a data da coluna {column}: {e}")

# Função para aplicar normalização em todas as colunas relevantes
def normalize_dataframe(df, collection_name):
    for col in df.columns:
        if df[col].dtype == 'object':
            if df[col].str.contains(',').any():
                print(f"Normalizando coluna {col} na coleção {collection_name}")
                normalize_comma_numbers(df, col)
        if 'date' in col.lower():
            print(f"Normalizando coluna de data {col} na coleção {collection_name}")
            normalize_dates(df, col)

# Função para obter DataFrame de uma coleção e aplicar normalização
def get_and_normalize_collection_df(collection_name):
    collection = db[collection_name]
    data = list(collection.find())
    df = pd.DataFrame(data)
    
    if not df.empty:
        normalize_dataframe(df, collection_name)
    return df

# Obter e normalizar DataFrames das collections
df_airflow = get_and_normalize_collection_df("airflow")
df_levels = get_and_normalize_collection_df("levels")
df_laboratory = get_and_normalize_collection_df("laboratory")
df_processvariables = get_and_normalize_collection_df("processvariables")

# Verificar se a coluna 'date' existe antes de realizar operações nela
if 'date' in df_airflow.columns:
    df_airflow['date'] = pd.to_datetime(df_airflow['date'])

if 'date' in df_levels.columns:
    df_levels['date'] = pd.to_datetime(df_levels['date'])

if 'date' in df_laboratory.columns:
    df_laboratory['date'] = pd.to_datetime(df_laboratory['date'])

if 'date' in df_processvariables.columns:
    df_processvariables['date'] = pd.to_datetime(df_processvariables['date'])

# Agregar os DataFrames usando o campo '_id' como chave
df_merged = pd.merge(df_airflow, df_levels, on='_id', how='outer', suffixes=('_airflow', '_levels'))
df_merged = pd.merge(df_merged, df_laboratory, on='_id', how='outer', suffixes=('', '_laboratory'))
df_merged = pd.merge(df_merged, df_processvariables, on='_id', how='outer', suffixes=('', '_processvariables'))

# Exibir o DataFrame final agregado
print(df_merged.head())
