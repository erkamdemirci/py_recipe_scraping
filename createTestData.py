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


def random_date(start):
    current = start
    curr = current + \
        datetime.timedelta(minutes=randrange(
            60), hours=randrange(24), days=randrange(240))
    return curr


startDate = datetime.datetime(2020, 1, 1, 1, 00)


def removekey(d, key):
    r = dict(d)
    del r[key]
    return r


testRecipes = []
hashes = []
img_files = glob.glob("./recipeImages/*.jpg")
for fileName in img_files[:30]:
    hash = fileName.split("/")[-1].replace(".jpg", "")
    hashes.append(hash)
    copy(fileName, "./test/images")
    for recipe in recipes:
        if recipe["linkHash"] == hash:
            recipe["likeCount"] = random.randint(500, 15000)
            recipe["commentCount"] = random.randint(5, 500)
            recipe["bookAdded"] = random.randint(150, 1000)
            recipe["createdAt"] = random_date(
                startDate).strftime("%d/%m/%y %H:%M")
            recipe["id"] = hash
            recipe = removekey(recipe, "linkHash")
            testRecipes.append(recipe)


with open('./test/testRecipes.json', 'w', encoding='utf8') as outfile:
    json.dump(testRecipes, outfile, ensure_ascii=False)
