import json
import glob
import os
from shutil import copy
import random

from random import randrange
import datetime

recipes = []
with open("recipesupload.json", encoding='utf8') as json_file:
    recipes = json.load(json_file)

_recipes = []
for recipe in recipes:
    textData = ""
    try:
        textData += recipe["descriptionPreContent"]
    except:
        pass
    for part in recipe["parts"]:
        try:
            textData += part["contentText"]
        except:
            try:
                for step in part["contentList"]:
                    textData += step["stepText"]
            except:
                pass

    try:
        _ingredients = []
        for ingredient in recipe["ingredients"]:
            ingredientObj = ingredient
            _subIngredients = []
            for subIngredient in ingredient["subIngredients"]:
                subIngredientObj = subIngredient
                recipeItemQty = subIngredient["recipeItemQty"]
                recipeItemQty = recipeItemQty.replace("g ", "gr.").replace(" gr", "gr.").replace(
                    " g", "gr.").replace(" g.", "gr.").replace("g.", "gr.").replace(" gr", "gr.")
                recipeItemQty = recipeItemQty.replace("ml ", "ml. ").replace(
                    " ml", "ml.").replace(" mililitre", "ml.").replace(" ml.", "ml.")
                recipeItemQty = recipeItemQty.replace("l ", "litre").replace(
                    " l", "litre").replace(" l.", "litre").replace("l. ", "litre")
                subIngredientObj["recipeItemQty"] = recipeItemQty
                _subIngredients.append(subIngredientObj)
            ingredientObj["subIngredients"] = _subIngredients
            _ingredients.append(ingredientObj)

        recipe["ingredients"] = _ingredients
    except:
        pass

    if "yemek.com" not in textData and "lezzet.com" not in textData and recipe["category"] != "Video Tarifleri":
        _recipes.append(recipe)

print(len(_recipes))
print(_recipes[50])
print(_recipes[15551])
print(_recipes[22222])
print(_recipes[8519])
with open('./recipes__.json', 'w', encoding='utf8') as outfile:
    json.dump(_recipes, outfile, ensure_ascii=False)
