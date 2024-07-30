import requests
import json
import os

def generate_menu(theme: str, number_of_courses: int):
    # Define the API endpoint and your API key
    api_url = "https://api.openai.com/v1/chat/completions"
    api_key = os.getenv("OPENAI_API_KEY")

    # Define the headers for the API request
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    # Define the payload for the API request
    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "Du bist ein Menü-Assistent. Deine Aufgabe ist es, basierend auf dem Thema und der Anzahl der Gänge, die der Benutzer vorgibt, ein Menü zu erstellen."},
            {"role": "user", "content": f"Erstelle ein Menü zum Thema '{theme}' mit {number_of_courses} Gängen. Gib nur die Namen der Gerichte als JSON-Array ohne weitere Erklärungen oder Formatierungen zurück."}
        ],
        "max_tokens": 150,
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
        menu_text = response_data['choices'][0]['message']['content']
        print("Menu text from API:", menu_text)
        menu_data = json.loads(menu_text)
        print("Parsed menu data:", menu_data)

            

# Beispielaufruf
theme = "weihnachtlich"
number_of_courses = 5
print("Generated menu:", generate_menu(theme, number_of_courses))
