import requests
from requests.auth import HTTPBasicAuth

# Set up your credentials and base URL
username = 'nachhaltigkeit'
password = 'cEh95KCC!3zrGtf@JR6R'
base_url = 'https://ecommerce-api.rewe.de/recipesearch/'

# Function to search for recipes
def search_recipes(search_term='', difficulty=None, max_cooking_time=None, min_cooking_time=None, objects_per_page=10, page=1, sorting='RELEVANCE_DESC', tags=None, tag_concat='OR'):
    endpoint = f'{base_url}recipes'
    params = {
        'searchTerm': search_term,
        'difficulty': difficulty,
        'maxCookingTime': max_cooking_time,
        'minCookingTime': min_cooking_time,
        'objectsPerPage': objects_per_page,
        'page': page,
        'sorting': sorting,
        'tag': tags,
        'tagConcat': tag_concat
    }
    
    response = requests.get(endpoint, params=params, auth=HTTPBasicAuth(username, password))
    if response.status_code == 200:
        return response.json()
    else:
        return response.status_code, response.text

# Function to get recipe details by ID
def get_recipe_by_id(recipe_id):
    endpoint = f'{base_url}recipes/{recipe_id}'
    response = requests.get(endpoint, auth=HTTPBasicAuth(username, password))
    if response.status_code == 200:
        return response.json()
    else:
        return response.status_code, response.text

# Function to get recipe details by name (slug)
def get_recipe_by_name(slug):
    endpoint = f'{base_url}recipes/by-name/{slug}'
    response = requests.get(endpoint, auth=HTTPBasicAuth(username, password))
    if response.status_code == 200:
        return response.json()
    else:
        return response.status_code, response.text

# Function to get all recipes
def get_all_recipes():
    page = 1
    all_recipes = []
    while True:
        search_result = search_recipes(objects_per_page=100, page=page)
        if 'recipes' in search_result:
            recipes = search_result['recipes']
            if not recipes:
                break
            for r in recipes:
                all_recipes.append({'id': r['id'], 'title': r['title']})
            page += 1
        else:
            break
    return all_recipes

# Function to get recipe steps by ID
def get_recipe_steps_by_id(recipe_id):
    recipe_detail = get_recipe_by_id(recipe_id)
    if isinstance(recipe_detail, dict) and 'preparation' in recipe_detail and 'steps' in recipe_detail['preparation']:
        return recipe_detail['preparation']['steps']
    else:
        return None



# Example usage
# if __name__ == '__main__':
#     # Search for recipes with the term 'steak'
#     search_result = search_recipes(search_term='steak', objects_per_page=5)
#     print("Search Result:", search_result)

#     # Get recipe details by ID
#     if 'recipes' in search_result and len(search_result['recipes']) > 0:
#         recipe_id = search_result['recipes'][0]['uuid']
#         recipe_detail = get_recipe_by_id(recipe_id)
#         print("Recipe Detail by ID:", recipe_detail)

#     # Get recipe details by name (slug)
#     if 'recipes' in search_result and len(search_result['recipes']) > 0:
#         recipe_slug = search_result['recipes'][0]['detailUrl'].split('/')[-1]
#         recipe_detail_by_name = get_recipe_by_name(recipe_slug)
#         print("Recipe Detail by Name:", recipe_detail_by_name)

