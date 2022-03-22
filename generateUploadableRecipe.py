import json
from os import confstr, name
from Crypto import Random
from Crypto.Cipher import AES
import base64
import random
from random import randrange
import datetime


class PKCS7Encoder():
    class InvalidBlockSizeError(Exception):
        pass

    def __init__(self, block_size=16):
        if block_size < 2 or block_size > 255:
            raise PKCS7Encoder.InvalidBlockSizeError('The block size must be '
                                                     'between 2 and 255, inclusive')
        self.block_size = block_size

    def encode(self, text):
        text_length = len(text)
        amount_to_pad = self.block_size - (text_length % self.block_size)
        if amount_to_pad == 0:
            amount_to_pad = self.block_size
        pad = chr(amount_to_pad)
        return text + pad * amount_to_pad

    def decode(self, text):
        pad = ord(text[-1])
        return text[:-pad]


def encrypt_val(clear_text):
    master_key = b'1234567890123456'
    encoder = PKCS7Encoder()
    raw = encoder.encode(clear_text)
    iv = Random.new().read(16)
    cipher = AES.new(master_key, AES.MODE_CBC, iv)
    return base64.b64encode(iv + cipher.encrypt(raw.encode("utf-8"))).decode("utf-8")


def random_date(start):
    current = start
    curr = current + \
        datetime.timedelta(minutes=randrange(
            60), hours=randrange(24), days=randrange(240))

    monthInt = int(curr.strftime("%m"))
    month = "January" if monthInt == 0 else "February" if monthInt == 1 else "March" if monthInt == 3 else "April" if monthInt == 4 else "May" if monthInt == 5 else "June" if monthInt == 6 else "July" if monthInt == 7 else "August"
    return curr.strftime(month+" %d, %y")


def removekey(d, key):
    r = dict(d)
    del r[key]
    return r


names = []
imageLinks = []
nameCounter = 0
with open("users.txt", encoding='utf8') as json_file:
    tmp = json_file.read()
    tmp = tmp.replace("'", '"')
    data = json.loads(tmp)

    for key in data:
        names.append(key)
        imageLinks.append(data[key])

recipes = []
with open("recipes.json", encoding='utf8') as json_file:
    recipes = json.load(json_file)

newRecipes = []
for recipe in recipes[:50]:
    startDate = datetime.datetime(2020, 1, 1, 1, 00)
    category = recipe["category"].title()

    recipe["owner"] = names[nameCounter]
    recipe["ownerImageKey"] = encrypt_val(imageLinks[nameCounter])
    recipe["recipeImageKey"] = encrypt_val(recipe["MainImage"])
    # recipe["createdAt"] = random_date(startDate).strftime("%d/%m/%y %H:%M")
    recipe["createdAt"] = random_date(startDate)
    recipe["id"] = recipe["linkHash"]
    recipe = removekey(recipe, "linkHash")
    recipe = removekey(recipe, "MainImage")
    recipe = removekey(recipe, "link")

    recipe["category"] = category
    newRecipes.append(recipe)

    nameCounter += 1
    if nameCounter == 53:
        nameCounter = 0


with open('./recipesupload.json', 'w', encoding='utf8') as outfile:
    json.dump(newRecipes, outfile, ensure_ascii=False)
