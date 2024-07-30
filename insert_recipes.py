from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import time
from rezepte_api import get_all_recipes

# Verbindung zu MongoDB Atlas herstellen
client = MongoClient("mongodb+srv://simon:AC8Sfs94aQGyocGv@cluster0.w6fudau.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0", server_api=ServerApi('1'))

db = client.recipes  # Verwenden Sie Ihren Datenbanknamen
collection = db.recipe_api  # Verwenden Sie Ihren Sammlungnamen


# Funktion, um Rezepte in Batches von 100 in die MongoDB zu speichern
'''
def insert_recipes_to_db(recipes):
    for i in range(0, len(recipes), 100):
        batch = recipes[i:i+100]
        try:
            collection.insert_many(batch)
            print(f"Inserted {len(batch)} recipes into the database.")
        except Exception as e:
            print(f"An error occurred while inserting recipes: {e}")
'''

# insert Ids with recipe id
def insert_recipes_to_db(recipes):
    for i in range(0, len(recipes), 100):
        batch = recipes[i:i+100]
        modified_batch = [{"_id": r["id"], "title": r["title"]} for r in batch]
        try:
            collection.insert_many(modified_batch)
            print(f"Inserted {len(modified_batch)} recipes into the database.")
        except Exception as e:
            print(f"An error occurred while inserting recipes: {e}")


all_recipes = get_all_recipes()
insert_recipes_to_db(all_recipes)