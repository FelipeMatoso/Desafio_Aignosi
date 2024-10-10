from pymongo import MongoClient
import pprint

string_conexao = "mongodb+srv://aignosi:SuperSecret!@desafioengdados.mongocluster.cosmos.azure.com/?tls=true&authMechanism=SCRAM-SHA-256&retrywrites=false&maxIdleTimeMS=120000"
client = MongoClient(string_conexao)

#Armzenando a Base de Dados e uma coleção em variaveis:
db = client["MiningProcess"]
collection_airflow = db["airflow"]
collection_levels = db["levels"]
collection_laboratory = db["laboratory"]
collection_processvariables = db["processvariables"]
pprint.pprint(collection_airflow.find_one())
pprint.pprint(collection_levels.find_one())
pprint.pprint(collection_laboratory.find_one())
pprint.pprint(collection_processvariables.find_one())
