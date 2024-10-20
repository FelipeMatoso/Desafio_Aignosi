import mysql.connector
from pymongo import MongoClient
import pandas as pd
from bson import ObjectId

# Conexão com MongoDB
string_conexao_mongo = "mongodb+srv://aignosi:SuperSecret!@desafioengdados.mongocluster.cosmos.azure.com/?tls=true&authMechanism=SCRAM-SHA-256&retrywrites=false&maxIdleTimeMS=120000"
client = MongoClient(string_conexao_mongo)
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

cnx = mysql.connector.connect(
    host='127.0.0.1',
    user='root',
    password='admin'
)
cursor = cnx.cursor()

# Criar o banco de dados se não existir
cursor.execute("CREATE DATABASE IF NOT EXISTS projeto_aignosi")
cnx.commit()

# Conectar ao banco de dados recém-criado
cnx.database = 'projeto_aignosi'

# Funções para criar tabelas das collections individuais no MySQL

def create_table_airflow(cursor, cnx):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS airflow (
            _id VARCHAR(255) PRIMARY KEY,
            date DATETIME,
            Flotation_Column_01_Air_Flow FLOAT,
            Flotation_Column_02_Air_Flow FLOAT,
            Flotation_Column_03_Air_Flow FLOAT,
            Flotation_Column_04_Air_Flow FLOAT,
            Flotation_Column_05_Air_Flow FLOAT,
            Flotation_Column_06_Air_Flow FLOAT,
            Flotation_Column_07_Air_Flow FLOAT
        );
    """)
    cnx.commit()

def create_table_levels(cursor, cnx):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS levels (
            _id VARCHAR(255) PRIMARY KEY,
            date DATETIME,
            Flotation_Column_01_Level FLOAT,
            Flotation_Column_02_Level FLOAT,
            Flotation_Column_03_Level FLOAT,
            Flotation_Column_04_Level FLOAT,
            Flotation_Column_05_Level FLOAT,
            Flotation_Column_06_Level FLOAT,
            Flotation_Column_07_Level FLOAT
        );
    """)
    cnx.commit()

def create_table_laboratory(cursor, cnx):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS laboratory (
            _id VARCHAR(255) PRIMARY KEY,
            Iron_Feed_Percentage FLOAT,
            Silica_Feed_Percentage FLOAT
        );
    """)
    cnx.commit()

def create_table_processvariables(cursor, cnx):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS processvariables (
            _id VARCHAR(255) PRIMARY KEY,
            date DATETIME,
            Amina_Flow FLOAT,
            Ore_Pulp_Density FLOAT,
            Ore_Pulp_Flow FLOAT,
            Ore_Pulp_pH FLOAT,
            Starch_Flow FLOAT
        );
    """)
    cnx.commit()

# Função para inserir dados nas tabelas individuais do MySQL
def insert_data_to_mysql(df, table_name, columns):
    for index, row in df.iterrows():
        # Converter ObjectId para string, se necessário
        row_to_insert = [str(row[col]) if isinstance(row[col], ObjectId) else row[col] for col in columns]
        
        # Usar backticks para colunas com espaços
        columns_sql = ', '.join([f"`{col}`" for col in columns])
        placeholders = ', '.join(['%s'] * len(columns))
        sql = f"INSERT INTO {table_name} ({columns_sql}) VALUES ({placeholders})"
        
        cursor.execute(sql, tuple(row_to_insert))
    cnx.commit()

# Criar tabelas no MySQL
create_table_airflow(cursor, cnx)
create_table_levels(cursor, cnx)
create_table_laboratory(cursor, cnx)
create_table_processvariables(cursor, cnx)

# Inserir dados nas tabelas correspondentes
insert_data_to_mysql(df_airflow, 'airflow', ['_id', 'date', 'Flotation Column 01 Air Flow', 'Flotation Column 02 Air Flow', 'Flotation Column 03 Air Flow', 'Flotation Column 04 Air Flow', 'Flotation Column 05 Air Flow', 'Flotation Column 06 Air Flow', 'Flotation Column 07 Air Flow'])
insert_data_to_mysql(df_levels, 'levels', ['_id', 'date', 'Flotation Column 01 Level', 'Flotation Column 02 Level', 'Flotation Column 03 Level', 'Flotation Column 04 Level', 'Flotation Column 05 Level', 'Flotation Column 06 Level', 'Flotation Column 07 Level'])
insert_data_to_mysql(df_laboratory, 'laboratory', ['_id', 'Iron Feed Percentage', 'Silica Feed Percentage'])
insert_data_to_mysql(df_processvariables, 'processvariables', ['_id', 'date', 'Amina Flow', 'Ore Pulp Density', 'Ore Pulp Flow', 'Ore Pulp pH', 'Starch Flow'])

# Fechar a conexão
cursor.close()
cnx.close()

# Exibir o DataFrame final agregado para verificar
# print(df_merged.head())
