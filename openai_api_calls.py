import instructor
from pydantic import BaseModel
from openai import OpenAI
import os
from typing import List, Iterable
from schema import Course, CourseLLM, Menu, RecipeStep
import json

theme = "ein winterliches Menü"
number_of_courses = 4

# Patch the OpenAI client
client = instructor.from_openai(OpenAI(api_key=os.getenv("OPENAI_API_KEY")))

########################################################################
# Maybe another pre-promt to format the original user prompt for the LLM
########################################################################

#  Generate The initial Menu from user prompt
def generate_menu(theme, number_of_courses):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        response_model=List[CourseLLM],
        messages=[
                {"role": "user", "content": f"Erstelle ein Menü zum Thema {theme} mit{number_of_courses} Gängen"},
                ],
        max_tokens=300,
        temperature=0.7,
    )
    print(response)
    return response
 
def get_step_durations(menu: Menu):

    # Bereite die Schritte für den API-Call vor
    steps = []
    for course in menu.courses:
        for step in course.steps:
            steps.append(step.description)

    menu = client.chat.completions.create(
        model="gpt-3.5-turbo",
        response_model=Menu,
        messages=[
            {"role": "system", "content": "Du bist ein Kochassistent. Deine Aufgabe ist es, die geschätzte Dauer für jeden Kochschritt zu bestimmen."},
            {"role": "user", "content": f"Hier sind die Schritte eines Menüs:\n{json.dumps(steps, indent=2)}\nGib mir die geschätzte Dauer in Minuten für jeden Schritt als RecipeStep.duration zurück wobei die Reihenfolge der Schritte beibehalten wird."}
        ],
            max_tokens=1000,
            temperature=0.7,
    )
    return menu
    
   

