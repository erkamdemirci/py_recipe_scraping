import enum
import json
import requests
from sys import getsizeof
import re


# upload recipes to "recipes" collection
createRecipeDocURL = '' 
recipes = []

# with open("recipesupload.json", encoding='utf8') as json_file:
#     recipes = json.load(json_file)

firebaseRecipes = []
with open("firebaseRecipes.json", encoding='utf8') as json_file:
    firebaseRecipes = json.load(json_file)


# counter = 0
# for recipe in recipes:
#     counter += 1
#     x = requests.post(createRecipeDocURL, json=recipe).json()
#     recipe["firestoreID"] = x["id"]
#     print(counter)
#     firebaseRecipes.append(recipe)

IDsAndFirestoreIDs = {}

wordCounts = {}
categories = {}
firebaseCategoriesDoc = {}
categoryRecipeCounts = {}
for recipe in firebaseRecipes:
    category = recipe["category"].replace(" Tarifi", "").replace(
        " Tarifleri", "").replace(" Tarifler", "").replace(" Yemeği", "").replace("i̇", "i")
    category = category.lower()
    category = category.replace("i̇", "i")
    category = category.lstrip().rstrip()
    categoryWords = category.split(" ")

    searchTerm = recipe["titleSecond"].replace(" Tarifi", "").replace(
        " Tarifleri", "").replace(" Tarifler", "").replace(" Yemeği", "")
    searchTerm = searchTerm.lower()
    searchTerm = searchTerm.replace("i̇", "i")
    searchTerm = ''.join([i for i in searchTerm if not i.isdigit()])
    searchTerm = re.sub('\s+', ' ', searchTerm)
    firestoreID = recipe["firestoreID"]

    for word in category.split():
        if word not in searchTerm:
            searchTerm += " " + word

    searchTerm = re.sub(
        r"([\.\,\\\+\*\?\[\^\]\$\(\)\{\}\!\<\>\|\:\-])", "", searchTerm)
    _searchTerm = ""
    for word in searchTerm.split():
        _searchTerm += word + " "

    searchTerm = _searchTerm.lstrip().rstrip()
    for term in searchTerm.split():
        if term not in wordCounts:
            wordCounts[term] = 1
        else:
            wordCounts[term] += 1

    category = recipe["category"].lstrip().rstrip()
    if category not in categories:
        categoryRecipeCounts[category] = 1
        categories[category] = [firestoreID]
    else:
        categoryRecipeCounts[category] += 1
        categories[category].append(firestoreID)

firebaseCategoriesDoc["categoryRecipeCounts"] = categoryRecipeCounts
firebaseCategoriesDoc["categories"] = categories

wordObjects = {}
# en çok geçen kelimelere en küçük indexin verildiği obje (wordObjects)
sortedWordCounts = sorted(wordCounts.items(), key=lambda x: x[1], reverse=True)
for i, j in enumerate(sortedWordCounts):
    wordObjects[j[0]] = i  # wordObjects["tatlı"] = 0 - en çok geçen kelime

cryptedSearchWords = {}

for recipe in firebaseRecipes:
    category = recipe["category"].replace(" Tarifi", "").replace(
        " Tarifleri", "").replace(" Tarifler", "").replace(" Yemeği", "").replace("i̇", "i")
    category = category.lower()
    category = category.replace("i̇", "i")
    category = category.lstrip().rstrip()
    categoryWords = category.split(" ")

    searchTerm = recipe["titleSecond"].replace(" Tarifi", "").replace(
        " Tarifleri", "").replace(" Tarifler", "").replace(" Yemeği", "")
    searchTerm = searchTerm.lower()
    searchTerm = searchTerm.replace("i̇", "i")
    searchTerm = ''.join([i for i in searchTerm if not i.isdigit()])
    searchTerm = re.sub('\s+', ' ', searchTerm)
    firestoreID = recipe["firestoreID"]

    for word in category.split():
        if word not in searchTerm:
            searchTerm += " " + word

    searchTerm = re.sub(
        r"([\.\,\\\+\*\?\[\^\]\$\(\)\{\}\!\<\>\|\:\-])", "", searchTerm)
    _searchTerm = ""
    for word in searchTerm.split():
        _searchTerm += word + " "

    searchTerm = _searchTerm.lstrip().rstrip()
    for term in searchTerm.split():
        searchTerm = searchTerm.replace(term, str(wordObjects[term]))

    for term in searchTerm.split():
        _obj = {"firestoreID": firestoreID, "title": searchTerm}
        if str(term) not in cryptedSearchWords:
            cryptedSearchWords[str(term)] = [_obj]
        else:
            cryptedSearchWords[str(term)].append(_obj)



with open('./cryptedSearchWords.json', 'w', encoding='utf8') as outfile:
    json.dump(cryptedSearchWords, outfile, ensure_ascii=False)

with open('./sortedWordCounts.json', 'w', encoding='utf8') as outfile:
    json.dump(sortedWordCounts, outfile, ensure_ascii=False)

with open('./wordObjects.json', 'w', encoding='utf8') as outfile:
    json.dump(wordObjects, outfile, ensure_ascii=False)

with open('./firebaseCategoriesDoc.json', 'w', encoding='utf8') as outfile:
    json.dump(firebaseCategoriesDoc, outfile, ensure_ascii=False)

# keys = cryptedSearchWords.keys()
# objArr = []
# counter = 1
# obj = {}
# for key in keys:
#     if counter > 50:
#         counter = 1
#         objArr.append(obj)
#         obj = {}
#     obj[key] = cryptedSearchWords[key]
#     counter += 1

# counter = 1
# for obj in objArr:
#     print(counter*50)
#     counter += 1
#     # upload searchTerms collection as single doc
#     r = requests.post(
#         "http://localhost:5001/recipe-app-34e89/us-central1/app/api/createCryptedSearchTermDocs", json=obj)
# print("DONE# create and upload new createCryptedSearchTermDocs doc")

# # upload searchTerms collection as single doc
# r = requests.post(
#     "http://localhost:5001/recipe-app-34e89/us-central1/app/api/createSearchWordKeyDictionary", json=wordObjects)
# print("DONE# create and upload new createSearchWordKeyDictionaryURL doc")

# upload categoriesAndRecipes collection as single doc
r = requests.post(
    URL, json=firebaseCategoriesDoc)
