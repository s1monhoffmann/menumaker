import os
import requests
import json
from schema import Menu, Course, RecipeStep

def sort_steps(menu: Menu):
    # Define the API endpoint and your API key
    api_url = "https://api.openai.com/v1/chat/completions"
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        print("API key not found.")
        return None

    # Define the headers for the API request
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    # Bereite die Schritte für den API-Call vor
    steps = []
    for course in menu.courses:
        for step in course.steps:
            steps.append({
                "step_number": step.step_number,
                "description": step.description,
                "duration": step.duration
            })

    # Define the payload for the API request
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "Du bist ein Kochassistent. Deine Aufgabe ist es, die Kochschritte basierend auf ihrer Dauer und Priorität zu sortieren. Schritte, die lange dauern (z.B. Einweichen von Bohnen), sollten zuerst kommen. Schritte, die kurz vor dem Servieren erledigt werden sollten (z.B. Kartoffeln kochen), sollten am Ende kommen."},
            {"role": "user", "content": f"Hier sind die Schritte eines Menüs:\n{json.dumps(steps, indent=2)}\nGib mir die sortierten Schritte als JSON-Array zurück, wobei die Reihenfolge der Schritte beibehalten wird."}
        ],
        "max_tokens": 2000,
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
        sorted_steps_text = response_data['choices'][0]['message']['content']
        print("Sorted steps text from API:", sorted_steps_text)
        sorted_steps = json.loads(sorted_steps_text)
        print("Parsed sorted steps data:", sorted_steps)

        # Update the steps in the Pydantic object
        for course in menu.courses:
            course.steps = []
        for step_data in sorted_steps:
            step = RecipeStep(
                step_number=step_data["step_number"],
                description=step_data["description"],
                duration=step_data["duration"]
            )
            for course in menu.courses:
                if not course.steps or course.steps[-1].step_number < step.step_number:
                    course.steps.append(step)
                    break

        return menu
    else:
        print("API request failed with status code:", response.status_code)
        print("Response:", response.text)
        return None
