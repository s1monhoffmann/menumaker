import instructor
from pydantic import BaseModel
from openai import OpenAI
import os
from typing import List, Iterable
from schema import Course, Menu, RecipeStep, CourseLLM
import json

theme = "ein winterliches Menü"
number_of_courses = 4

# Patch the OpenAI client
client = instructor.from_openai(OpenAI(api_key=os.getenv("OPENAI_API_KEY")))

def generate_menu(theme, number_of_courses):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        response_model=Iterable[CourseLLM],
        messages=[
                {"role": "user", "content": f"Erstelle ein Menü zum Thema {theme} mit{number_of_courses} Gängen"},
                ],
        max_tokens=300,
        temperature=0.7,
    )
    print(response)
 #   menu = Menu(courses=response)
 #   return menu


def get_step_durations(menu: Menu):

    
    menu = client.chat.completions.create(
        model="gpt-3.5-turbo",
        response_model=Iterable,
        messages=[
            
            {"role": "user", "content": f"git mir für den RecipieStep die dauer in Minuten zurück die es braucht den Schritt zu bearbeiten. "}      ],
            max_tokens=1000,
            temperature=0.7,
    )
    return menu
    
   
theme = "ein winterliches Menü"
number_of_courses = 7
menu = generate_menu(theme, number_of_courses)
print(menu)