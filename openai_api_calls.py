import instructor
from pydantic import BaseModel
from openai import OpenAI
import os
from typing import List
from schema import Course, Menu, RecipeStep, SortedRecipeStep
import json

theme = "ein winterliches Menü"
number_of_courses = 4

# Patch the OpenAI client
client = instructor.from_openai(OpenAI(api_key=os.getenv("OPENAI_API_KEY")))

############################################
# Villeicht Query Pydanitc um Frage richtig zu forma

# Extract structured data from natural language
def generate_menu(theme, number_of_courses):
    menu = client.chat.completions.create(
        model="gpt-3.5-turbo",
        response_model=Menu,
        messages=[
                {"role": "system", "content": "Du bist ein Menü-Assistent. Deine Aufgabe ist es, basierend auf dem Thema und der Anzahl der Gänge, die der Benutzer vorgibt, ein Menü zu erstellen."},
            
                {"role": "user", "content": f"Erstelle ein Menü zum Thema '{theme}' mit {number_of_courses} Gängen. Gib die Namen der Gerichte für die einzelnen Gänge als llm_name der Course-Objekte zurück, ohne weitere Erklärungen oder Formatierungen. Beispiel: Caprese-Salat, Gegrilltes Hähnchen mit Gemüse, usw."}

            ],
            max_tokens=300,
            temperature=0.5,
    )
    return menu

# def get_step_durations(menu: Menu):

#     # Bereite die Schritte für den API-Call vor
#     steps = []
#     for course in menu.courses:
#         for step in course.steps:
#             steps.append(step.description)

#     menu = client.chat.completions.create(
#         model="gpt-3.5-turbo",
#         response_model=Menu,
#         messages=[
#             {"role": "system", "content": "Du bist ein Kochassistent. Deine Aufgabe ist es, die geschätzte Dauer für jeden Kochschritt zu bestimmen."},
#             {"role": "user", "content": f"Hier sind die Schritte eines Menüs:\n{json.dumps(steps, indent=2)}\nGib mir die geschätzte Dauer in Minuten für jeden Schritt als RecipeStep.duration zurück wobei die Reihenfolge der Schritte beibehalten wird."}
#         ],
#             max_tokens=1000,
#             temperature=0.7,
#     )
#     return menu
    
   
def get_step_durations(menu: Menu):
    menu_dict = menu.dict()
    menu = client.chat.completions.create(
        model="gpt-4o-mini",
        response_model=Menu,
        messages=[
            {"role": "user", "content": f"Bitte füge zu den Schritten/RecipeSteps dieses Menüs :\n{json.dumps(menu_dict, indent=2)}\n noch die duration in Minuten die es braucht den einzelnen Schreitt zu bearbeiten sonst übernehme alle Daten so wie sie sind ins Menu Objekt."}
        ],
            max_tokens=3000,
            temperature=0.7,
    )
    return menu


def get_step_order(menu: Menu) -> List[SortedRecipeStep]:
    menu_dict = menu.dict()
    response = client.chat.completions.create(
        model="gpt-4o",
        response_model=List[SortedRecipeStep],
        messages=[
            {
                "role": "user",
                "content": f"""
Ich habe ein Menü mit mehreren Gängen, und jeder Gang hat eine Liste von Rezeptschritten (RecipeSteps). Diese Schritte sind momentan unsortiert. Bitte ordne alle Schritte des Menüs so, dass die Zubereitung in einer logischen Reihenfolge erfolgt.

Berücksichtige dabei:
- Schritte, die eine lange Vorbereitungszeit erfordern, sollten früh beginnen (z. B. Bohnen einweichen).
- Schritte, die kurz vor dem Servieren durchgeführt werden müssen, sollten spät erfolgen (z. B. Kartoffeln kochen).

Hier ist das Menü:

{json.dumps(menu_dict, indent=2)}

Füge jedem Rezeptschritt eine `step_number` hinzu, die die Reihenfolge der Schritte widerspiegelt. Alle anderen Daten sollen unverändert bleiben.
                """
            }
        ],
        max_tokens=3000,
        temperature=0.7,
    )
    return response