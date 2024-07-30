from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# Verbindung zu MongoDB Atlas herstellen
client = MongoClient("mongodb+srv://simon:AC8Sfs94aQGyocGv@cluster0.w6fudau.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0", server_api=ServerApi('1'))

db = client.recipes  
collection = db.recipe_api 

