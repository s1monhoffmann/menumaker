import json, time
from schema import Course, Menu, RecipeStep
from openai_api_calls import generate_menu, get_step_durations, get_step_order
from queries import get_similar_recipes
from rezepte_api import get_recipe_steps_by_id
# from order_of_steps_api_call import sort_steps

BASE_URL = 'https://ecommerce-api.rewe.de/recipesearch/'

if __name__ == '__main__':
    
    # Generate menu
    start_time_llm_name = time.time()

    theme = "ich will ein sommerliches Menü kochen"
    number_of_courses = 4
    menu = generate_menu(theme, number_of_courses)
    
    print(f"Inaitial menu generation took {time.time() - start_time_llm_name} seconds")
    print('generated menu',menu)



    # Get recipe info form REWE Rezepte API
    start_time_get_recipe_info = time.time()

    step_counter = 1 
    for course in menu.courses:
        # Holen des ähnlichen Rezepts aus der Vektordatenbank
        results = get_similar_recipes(course.llm_name)
        similar_recipe = next(results, None)  # Holen des ersten (und einzigen) Ergebnisses

        if similar_recipe:
            # Get the recipe id and name
            course.id = str(similar_recipe["_id"]) 
            course.recipe_api_name = similar_recipe["title"]

            # Create link
            course.link = f'{BASE_URL}recipes/{course.id}'

            # Get the recipe steps
            steps = get_recipe_steps_by_id(course.id)
            course.steps = [RecipeStep(step_number=step_counter + i, description=step["description"]) for i, step in enumerate(steps) if "description" in step]
            step_counter += len(course.steps)  # Update den Schrittzähler

    print(f"Getting recipe info took {time.time() - start_time_get_recipe_info} seconds")
    print("Menü id, name, link und Rezept-Schritte", menu)

    # convert all steps to a json object and print it
    menu_dict = menu.dict()
    # print(json.dumps(menu_dict, indent=2))

    # Get step durations
    start_time_get_steps_duration = time.time()

    menu_with_duration_of_steps = get_step_durations(menu)
    print(menu_with_duration_of_steps)
    print(f"Getting step durations took {time.time() - start_time_get_steps_duration} seconds")

    # Sort steps returns List[SortedRecipeStep]
    start_time_sort_steps = time.time()
    sorted_steps  = get_step_order(menu_with_duration_of_steps)
    
    # Durchlaufe die Liste und drucke jedes Objekt
    for step in sorted_steps:
        print(f"Schritt {step.step_number}: {step.description} (Dauer: {step.duration} Minuten)")
    print(f"Sorting steps took {time.time() - start_time_sort_steps} seconds")

    

#    #Ausgabe des aktualisierten Menüs
#     for course in menu_with_sorted_steps.courses:
#         print(f"Course ID: {course.id}")
#         print(f"LLM Name: {course.llm_name}")
#         print(f"Recipe API Name: {course.recipe_api_name}")
#         print(f"Link: {course.link}")
#         print("Steps:")
#         for step in course.steps:
#             print(f"  {step.step_number}. {step.description}")
#         print()

    
    menu_dict = menu_with_duration_of_steps.dict()
    print(json.dumps(menu_dict, indent=2))