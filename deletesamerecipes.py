import json
import glob
import os
from shutil import copy
import random

from random import randrange
import datetime

recipes = []
with open("recipes.json", encoding='utf8') as json_file:
    recipes = json.load(json_file)

ids = []
newRecipes = []
for recipe in recipes:
    if recipe["link"] not in ids:
        ids.append(recipe["link"])
        newRecipes.append(recipe)
    else:
        print(recipe["link"])
print(len(newRecipes))
