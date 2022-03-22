import json
import glob
import os
from shutil import copy
import random

from random import randrange
import datetime

recipes = []
with open("recipes_smp.json", encoding='utf8') as json_file:
    recipes = json.load(json_file)

categories = []
categoryRecipeCounts = {}
for recipe in recipes:
    categoryT = recipe["category"].lower().replace(" ", "")
    category = recipe["category"]
    if category[-1] == " ":
        category = category[:-1]
    if categoryT not in categories:
        print(category.title())
        categoryRecipeCounts[category] = 1
        categories.append(categoryT)
    else:
        categoryRecipeCounts[category] += 1

for key in categoryRecipeCounts:
    with open('./categories_smp.txt', 'a+') as outfile:
        outfile.write(str(categoryRecipeCounts[key])+" , "+key+"\n")
