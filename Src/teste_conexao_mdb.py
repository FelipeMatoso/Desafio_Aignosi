from pymongo import MongoClient

#Conexão com URL fornecida:
string_conexao = "mongodb+srv://aignosi:SuperSecret!@desafioengdados.mongocluster.cosmos.azure.com/?tls=true&authMechanism=SCRAM-SHA-256&retrywrites=false&maxIdleTimeMS=120000"
#Avisos de efetividade da conexão mais listamento do nome da base de dados e de suas collections:
try:
    client = MongoClient(string_conexao)
    db = client["MiningProcess"]
    print("Conexão bem-sucedida!")
    print("Bancos de dados disponíveis:", client.list_database_names())
    print("Collections disponíveis:", db.list_collection_names())
except Exception as e:
    print(f"Erro na conexão: {e}")