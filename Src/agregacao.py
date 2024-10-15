import pandas as pd
from pymongo import MongoClient

# Conectar ao MongoDB
string_conexao = "mongodb+srv://aignosi:SuperSecret!@desafioengdados.mongocluster.cosmos.azure.com/?tls=true&authMechanism=SCRAM-SHA-256&retrywrites=false&maxIdleTimeMS=120000"
client = MongoClient(string_conexao)
db = client["MiningProcess"]

# Função para converter os dados de uma coleção em um DataFrame
def get_collection_df(collection_name):
    collection = db[collection_name]
    data = list(collection.find())
    df = pd.DataFrame(data)
    return df

# Obter DataFrames das collections
df_airflow = get_collection_df("airflow")
df_levels = get_collection_df("levels")
df_laboratory = get_collection_df("laboratory")
df_processvariables = get_collection_df("processvariables")

# Verificar se a coluna 'date' existe antes de realizar operações nela
if 'date' in df_airflow.columns:
    df_airflow['date'] = pd.to_datetime(df_airflow['date'])

if 'date' in df_levels.columns:
    df_levels['date'] = pd.to_datetime(df_levels['date'])

if 'date' in df_laboratory.columns:
    df_laboratory['date'] = pd.to_datetime(df_laboratory['date'])

if 'date' in df_processvariables.columns:
    df_processvariables['date'] = pd.to_datetime(df_processvariables['date'])

# Agregando os DataFrames usando o campo '_id' como chave
df_merged = pd.merge(df_airflow, df_levels, on='_id', how='outer', suffixes=('_airflow', '_levels'))
df_merged = pd.merge(df_merged, df_laboratory, on='_id', how='outer', suffixes=('', '_laboratory'))
df_merged = pd.merge(df_merged, df_processvariables, on='_id', how='outer', suffixes=('', '_processvariables'))

# Exibir o DataFrame final agregado
print(df_merged.head())
