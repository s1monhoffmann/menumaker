from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from embeddings_oa import generate_embeddings

import os

mongodb_user = os.getenv("MONGODB_USER")
mongodb_password = os.getenv("MONGODB_PASSWORD")

# Verbindung zu MongoDB Atlas herstellen
client = MongoClient(f"mongodb+srv://{mongodb_user}:{mongodb_password}@cluster0.w6fudau.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0", server_api=ServerApi('1'))

db = client.recipes  
collection = db.recipe_api 

def get_similar_recipes(course):
    query = course
    query_embedding = generate_embeddings(query)

    results = collection.aggregate([
        {"$vectorSearch": {
            "queryVector": query_embedding,
            "path": "title_embedding",
            "numCandidates": 100,
            "limit": 1,
            "index": "vector_index"
        }}
    ])


    return results

# Check connection
# try:
#     client.admin.command('ping')
#     print("Verbindung zu MongoDB Atlas erfolgreich hergestellt!")
# except Exception as e:
#     print(f"Fehler bei der Verbindung zu MongoDB Atlas: {e}")