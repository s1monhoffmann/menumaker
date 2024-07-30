import requests
import json
from schema import Menu, Course, RecipeStep

def get_step_durations(menu: Menu):
    # Define the API endpoint and your API key
    api_url = "https://api.openai.com/v1/chat/completions"
    api_key = os.getenv("OPENAI_API_KEY")

    # Define the headers for the API request
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    # Bereite die Schritte für den API-Call vor
    steps = []
    for course in menu.courses:
        for step in course.steps:
            steps.append(step.description)
    
    # Define the payload for the API request
    payload = {
        "model": "gpt-4",
        "messages": [
            {"role": "system", "content": "Du bist ein Kochassistent. Deine Aufgabe ist es, die geschätzte Dauer für jeden Kochschritt zu bestimmen."},
            {"role": "user", "content": f"Hier sind die Schritte eines Menüs:\n{json.dumps(steps, indent=2)}\nGib mir die geschätzte Dauer in Minuten für jeden Schritt als JSON-Array zurück, wobei die Reihenfolge der Schritte beibehalten wird."}
        ],
        "max_tokens": 300,
        "temperature": 0.7
    }

    # Make the API request
    response = requests.post(api_url, headers=headers, json=payload)

    # Check if the request was successful
    if response.status_code == 200:
        print("API request successful.")
        response_data = response.json()
        print("Raw response data:", response_data)
        
        # Parse the JSON response directly
        durations_text = response_data['choices'][0]['message']['content']
        print("Durations text from API:", durations_text)
        durations = json.loads(durations_text)
        print("Parsed durations data:", durations)

        # Füge die Dauer zu den Schritten im Pydantic-Objekt hinzu
        step_index = 0
        for course in menu.courses:
            for step in course.steps:
                if step_index < len(durations):
                    step.duration = durations[step_index]
                    step_index += 1

        return menu
    else:
        print("API request failed with status code:", response.status_code)
        print("Response:", response.text)
        return None

# Beispielaufruf
# Hier sollte dein bereits erstelltes Menü-Pydantic-Objekt verwendet werden
# Zum Beispiel:
# menu = generate_menu("mediteran", 4)
# Wir gehen davon aus, dass das 'menu' Objekt bereits existiert

# Füge die neuen Felder zum Pydantic-Modell hinzu, wenn sie noch nicht existieren
for course in menu.courses:
    for step in course.steps:
        step.duration = 0

updated_menu = get_step_durations(menu)
print(json.dumps(updated_menu.dict(), indent=2))