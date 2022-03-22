import json
import re
import keyboard
import os

recipes = []
with open("recipesupload.json", encoding='utf8') as json_file:
    recipes = json.load(json_file)

popularIngredientsBigList = []
with open("popular-ingredients-biglist.txt", encoding='utf8') as txt_file:
    popularIngredientsBigList = txt_file.readlines()
    for i, ingredient in enumerate(popularIngredientsBigList):
        popularIngredientsBigList[i] = ingredient.replace("\n", "")
    popularIngredientsBigList.sort(key=len)
    popularIngredientsBigList = popularIngredientsBigList[::-1]

extraIngredients = []
with open("extraIngredients.txt", encoding='utf8') as txt_file:
    extraIngredients = txt_file.readlines()
    for i, ingredient in enumerate(extraIngredients):
        extraIngredients[i] = ingredient.replace("\n", "")
    extraIngredients.sort(key=len)
    extraIngredients = extraIngredients[::-1]

qtynames = []
with open("qtynames.txt", encoding='utf8') as txt_file:
    qtynames = txt_file.readlines()
    for i, qtyname in enumerate(qtynames):
        qtynames[i] = qtyname.replace("\n", "")
    qtynames.sort(key=len)
    qtynames = qtynames[::-1]

completedIDs = []
if os.path.isfile("completed/completedIDs.txt"):
    with open("completed/completedIDs.txt", encoding='utf8') as txt_file:
        completedIDs = txt_file.readlines()
        for i, id in enumerate(completedIDs):
            completedIDs[i] = id.replace("\n", "")


def remove_emoji(string):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', string)


ingredients = {}
newRecipes = []
badRecipes = []
qtyNames = {}
counter = 0
totalCounter = 0
for recipe in recipes:
    passRecipe = False
    totalCounter += 1
    if not recipe["id"] in completedIDs:
        newSubingredientsArr = []
        for subIngredients in recipe["ingredients"]:
            if passRecipe:
                break
            newSubingredientObj = {}
            newSubingredientObj["subgradientTitle"] = subIngredients["subgradientTitle"]
            newIngredientsArr = []
            recipeItemNamesArr = []
            for subIngredient in subIngredients["subIngredients"]:
                if passRecipe:
                    break
                recipeItemNamesArr.append(
                    subIngredient["recipeItemName"])
                parenthesis = ""
                ingredientFlag = False
                passIngredient = False
                checkQtys = True
                newIngredientObj = subIngredient
                ingredientName = newIngredientObj["recipeItemName"].lower()
                ingredientName = remove_emoji(ingredientName)
                ingredientName = ingredientName.replace("  ", " ")
                ingredientName = ingredientName.lstrip().rstrip()
                index1 = ingredientName.find("(")
                index2 = ingredientName.find(")")
                if index1 != -1:
                    if index2 != -1:
                        parenthesis = ingredientName[index1+1:index2]
                        ingredientName = ingredientName[:index1] + \
                            ingredientName[index2+1:]
                        parenthesis = parenthesis.lstrip().rstrip()
                    else:
                        ingredientName = ingredientName[:index1]
                ingredientName = ingredientName.replace(
                    "  ", " ").replace("~", "-")
                ingredientName = ingredientName.lstrip().rstrip()

                ingredientFound = False
                newRecipeItemQty = ""
                newRecipeItemName = ""
                newIconName = ""

                if len(ingredientName) > 50:
                    passRecipe = True
                else:
                    if "recipeItemQty" not in newIngredientObj:
                        for i, qtyname in enumerate(qtynames):
                            if ingredientFound:
                                break

                            if parenthesis != "":
                                newIngredientObj["parenthesis"] = parenthesis

                            qtyname = qtyname.lstrip().rstrip()
                            if ingredientName.find(qtyname+" ") == 0:
                                newRecipeItemQty = qtyname
                                newRecipeItemName = ingredientName.replace(
                                    newRecipeItemQty, "")
                                newRecipeItemName = newRecipeItemName.lstrip().rstrip()

                                for _ingredient in popularIngredientsBigList:
                                    if newRecipeItemName == _ingredient:
                                        counter += 1

                                        newIngredientObj["iconName"] = newRecipeItemName
                                        if qtyname.lower().lstrip().rstrip() != "":
                                            if parenthesis in newRecipeItemQty:
                                                newRecipeItemQty = newRecipeItemQty.replace(
                                                    parenthesis, "").replace("  ", "").lstrip().rstrip()
                                            newIngredientObj["recipeItemQty"] = newRecipeItemQty
                                            newIngredientObj["recipeItemName"] = newRecipeItemName
                                            print(qtyname + " | " +
                                                  newRecipeItemName + " -> " + str(counter) + " ~ " + str(totalCounter))

                                            ingredientFound = True
                                        else:
                                            newIngredientObj["recipeItemName"] = newRecipeItemName
                                            print(newRecipeItemName +
                                                  " -> " + str(counter) + " ~ " + str(totalCounter))
                                        break
                                for _ingredient in extraIngredients:
                                    if newRecipeItemName == _ingredient:
                                        counter += 1

                                        newIngredientObj["iconName"] = newRecipeItemName
                                        if qtyname.lower().lstrip().rstrip() != "":
                                            if parenthesis in newRecipeItemQty:
                                                newRecipeItemQty = newRecipeItemQty.replace(
                                                    parenthesis, "").replace("  ", "").lstrip().rstrip()
                                            newIngredientObj["recipeItemQty"] = newRecipeItemQty
                                            newIngredientObj["recipeItemName"] = newRecipeItemName
                                            print(qtyname + " | " +
                                                  newRecipeItemName + " -> " + str(counter) + " ~ " + str(totalCounter))

                                            ingredientFound = True
                                        else:
                                            newIngredientObj["recipeItemName"] = newRecipeItemName
                                            print(newRecipeItemName +
                                                  " -> " + str(counter) + " ~ " + str(totalCounter))
                                        break
                                if not ingredientFound:
                                    while True:
                                        print(ingredientName +
                                              "\n\nQTY : "+newRecipeItemQty+"\nINGREDIENT : " + newRecipeItemName)
                                        os.system('read -s -n 1 -p ""')
                                        if keyboard.is_pressed('y'):
                                            counter += 1
                                            ingredientFound = True
                                            newIngredientObj["recipeItemQty"] = newRecipeItemQty
                                            newIngredientObj["recipeItemName"] = newRecipeItemName
                                            if newRecipeItemName not in extraIngredients:
                                                extraIngredients.append(
                                                    newRecipeItemName)
                                                extraIngredients.sort(key=len)
                                                extraIngredients = extraIngredients[::-1]
                                                f = open(
                                                    "extraIngredients.txt", "a+")
                                                f.write(newRecipeItemName+"\n")
                                                f.close()
                                            print("--> Değiştirildi")
                                            break
                                        elif keyboard.is_pressed('o'):
                                            break

                        if not ingredientFound:
                            print("[ " + ingredientName + " ]\n")
                            recipeItemQty = ""
                            recipeItemName = ""
                            tmp = ingredientName.split(" ")
                            if len(tmp) < 3 and not any(char.isdigit() for char in ingredientName):
                                recipeItemName = ingredientName
                            elif len(tmp) == 3 and not any(char.isdigit() for char in ingredientName):
                                recipeItemName = ingredientName
                            else:
                                recipeItemQty = input("recipeItemQty : ")
                                if recipeItemQty == "pass":
                                    passRecipe = True
                                    continue
                                elif recipeItemQty+" " in ingredientName and recipeItemQty != "":
                                    recipeItemName = ingredientName.replace(
                                        recipeItemQty, "")
                                    recipeItemName = recipeItemName.lstrip().rstrip()
                                elif recipeItemQty == "":
                                    recipeItemName = ingredientName
                                else:
                                    recipeItemName = input("recipeItemName : ")

                            recipeItemQty = recipeItemQty.lstrip().rstrip()
                            if recipeItemQty != "" and recipeItemQty not in qtynames:
                                qtynames.append(recipeItemQty)
                                qtynames.sort(key=len)
                                qtynames = qtynames[::-1]
                                f = open("qtynames.txt", "a+")
                                f.write(recipeItemQty+"\n")
                                f.close()
                                extraIngredients.append(newRecipeItemName)
                                extraIngredients.sort(key=len)
                                extraIngredients = extraIngredients[::-1]
                                f = open(
                                    "extraIngredients.txt", "a+")
                                f.write(newRecipeItemName+"\n")
                                f.close()
                            if recipeItemQty.lstrip().rstrip() != "":
                                newIngredientObj["recipeItemQty"] = recipeItemQty.lstrip(
                                ).rstrip()
                            newIngredientObj["recipeItemName"] = recipeItemName

                            ingredientFound = True
                            counter += 1

                        # for _ingredient in popularIngredientsBigList:
                        #     if ingredientFound:
                        #         break
                        #     if not _ingredient+" " in ingredientName and _ingredient in ingredientName and _ingredient:  # cümlenin sonundaysa, içinde varsa, boş değilse
                        #         control = ingredientName.split(_ingredient)
                        #         if len(control[-1]) < 2:
                        #             newRecipeItemQty = ingredientName.replace(
                        #                 _ingredient, "")
                        #             newRecipeItemQty = newRecipeItemQty.lstrip().rstrip()
                        #             newRecipeItemName = _ingredient.lstrip().rstrip()
                        #             newIngredientObj["iconName"] = newRecipeItemName
                        #             if parenthesis != "":
                        #                 newIngredientObj["parenthesis"] = parenthesis
                        #             tmpQtyName = ""
                        #             for qtyname in qtynames:
                        #                 if qtyname.lower().lstrip().rstrip() == newRecipeItemQty.lower().lstrip().rstrip():
                        #                     counter += 1
                        #                     ingredientFound = True
                        #                     if qtyname.lower().lstrip().rstrip() != "":
                        #                         newIngredientObj["recipeItemQty"] = qtyname.lower(
                        #                         ).lstrip().rstrip()
                        #                         newIngredientObj["recipeItemName"] = newRecipeItemName
                        #                         print(qtyname, newRecipeItemName)
                        #                     else:
                        #                         newIngredientObj["recipeItemName"] = newRecipeItemName
                        #                         print(newRecipeItemName)
                        #                     break

                newIngredientsArr.append(newIngredientObj)
            newSubingredientObj["subIngredients"] = newIngredientsArr
            newSubingredientsArr.append(newSubingredientObj)

        f = open("completed/completedIDs.txt", "a+")
        f.write(recipe["id"]+"\n")
        f.close()

        recipe["ingredients"] = newSubingredientsArr

        if not passRecipe:
            f = open("completed/completedRecipes.txt", "a+", encoding='utf8')
            f.write(json.dumps(recipe, ensure_ascii=False)+",")
            f.close()

print(counter)
