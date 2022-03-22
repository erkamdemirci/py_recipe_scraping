import json

recipes = []
with open("recipes.json", encoding='utf8') as json_file:
    recipes = json.load(json_file)

for recipe in recipes:
    print(recipe)
