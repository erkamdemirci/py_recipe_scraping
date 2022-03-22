import json

recipes = []
with open("recipes.json", encoding='utf8') as json_file:
    recipes = json.load(json_file)

categories = []
categoryRecipeCounts = {}
newRecipes = []
for recipe in recipes:
    category = recipe["category"].title()

    recipe["category"] = category
    newRecipes.append(recipe)

with open('./recipes_smp.json', 'w', encoding='utf8') as outfile:
    json.dump(newRecipes, outfile, ensure_ascii=False)
