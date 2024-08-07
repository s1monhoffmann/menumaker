import json
from schema import Course, Menu, RecipeStep
from openai_api_calls import generate_menu, get_step_durations
from queries import get_similar_recipes
from rezepte_api import get_recipe_steps_by_id
from order_of_steps_api_call import sort_steps

BASE_URL = 'https://ecommerce-api.rewe.de/recipesearch/'

if __name__ == '__main__':
    
    # Generate menu
    theme = "ich will ein sommerliches Menü kochen"
    number_of_courses = 4
    courses_llm = generate_menu(theme, number_of_courses)

    print(courses_llm)

    menu = Menu(coursesllm=courses_llm)
    print(menu)
    


    # # Füge ähnliche Rezepte und Schritte hinzu
    # step_counter = 1 
    # for course in menu.courses:
    #     # Holen des ähnlichen Rezepts aus der Vektordatenbank
    #     results = get_similar_recipes(course.llm_name)
    #     similar_recipe = next(results, None)  # Holen des ersten (und einzigen) Ergebnisses

    #     if similar_recipe:
    #         course.id = str(similar_recipe["_id"])  # sicherstellen, dass es ein String ist
    #         course.recipe_api_name = similar_recipe["title"]

    #         # Erstelle den Link
    #         course.link = f'{BASE_URL}recipes/{course.id}'

    #         # Holen der Rezeptschritte anhand der Rezept-ID
    #         steps = get_recipe_steps_by_id(course.id)
    #         course.steps = [RecipeStep(step_number=step_counter + i, description=step["description"]) for i, step in enumerate(steps) if "description" in step]
    #         step_counter += len(course.steps)  # Update den Schrittzähler


    #####################
    # Quatsch loop durch das Menü um dann einzelne api calls zu machen
    #####################

    # menu_with_duration_of_steps = get_step_durations(menu)
    # menu_with_sorted_steps = sort_steps(menu_with_duration_of_steps)

   # Ausgabe des aktualisierten Menüs
    # for course in menu.courses:
    #     print(f"Course ID: {course.id}")
    #     print(f"LLM Name: {course.llm_name}")
    #     print(f"Recipe API Name: {course.recipe_api_name}")
    #     print(f"Link: {course.link}")
    #     print("Steps:")
    #     for step in course.steps:
    #         print(f"  {step.step_number}. {step.description}")
    #     print()

    
    # menu_dict = menu_with_duration_of_steps.dict()
    # print(json.dumps(menu_dict, indent=2))