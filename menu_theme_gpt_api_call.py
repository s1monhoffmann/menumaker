import requests
import json
from pydantic import BaseModel
from typing import List
import time
from schema import Course, Menu, RecipeStep
import os

def generate_menu(theme, number_of_courses):
    # Define the API endpoint and your API key
    api_url = "https://api.openai.com/v1/chat/completions"
    api_key = os.getenv("OPENAI_API_KEY")


    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "Du bist ein Menü-Assistent. Deine Aufgabe ist es, basierend auf dem Thema und der Anzahl der Gänge, die der Benutzer vorgibt, ein Menü zu erstellen."},
            {"role": "user", "content": f"Erstelle ein Menü zum Thema '{theme}' mit {number_of_courses} Gängen. Gib nur die Namen der Gerichte als JSON-Array zurück, z.B. ['Salat', 'Schnitzel', 'Kuchen', 'Mousse au Chocolat'], keine weiteren Erklärungen oder Formatierungen. Achte darauf, dass die JSON-Antwort korrekt formatiert ist, mit doppelten Anführungszeichen um jeden Gerichtsnamen."}
        ],
        "max_tokens": 150,
        "temperature": 0.5
    }

    print("Sende Anfrage an die API...")
    start_time = time.time()

    # Make the API request
    response = requests.post(api_url, headers=headers, json=payload)

    end_time = time.time()
    duration = end_time - start_time

    print(f"Antwort erhalten mit Statuscode {response.status_code}")
    print(f"API-Aufruf dauerte {duration:.2f} Sekunden")


    if response.status_code == 200:
        response_data = response.json()
        # print("Antwort-JSON:", response_data)
        menu_text = response_data['choices'][0]['message']['content'].strip()
        # print("Menü-Text von der API:", menu_text)

        try:
            # Ersetzen Sie einfache Anführungszeichen
            menu_text = menu_text.replace("'", '"')

            course_names = json.loads(menu_text)
            courses = [Course(llm_name=name) for name in course_names]
            menu = Menu(courses=courses)
            return menu

        except json.JSONDecodeError as e:
            print("Fehler beim Parsen des JSON:", e)
            raise ValueError("Die Antwort des Modells konnte nicht als JSON geparst werden.")
    else:
        print("API-Anfrage fehlgeschlagen:", response.text)
        raise ValueError(f"API-Anfrage fehlgeschlagen mit Statuscode {response.status_code}: {response.text}")


# print(generate_menu("ein sommerliches Menü", 4))