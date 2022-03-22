import json

recipes = []
with open("recipesupload.json", encoding='utf8') as json_file:
    recipes = json.load(json_file)

print(len(recipes))

wordsObject = {}
for recipe in recipes:
    for part in recipe["parts"]:
        try:
            words = part["contentText"].replace("  ", " ")
            words = words.lower().replace(".", " ")
            words = words.replace("  ", " ")
            _words = words.split(" ")
            for i, word in enumerate(_words):
                if word in wordsObject:
                    wordsObject[word] += 1
                else:
                    wordsObject[word] = 1

        except:
            try:
                contentList = part["contentList"]
                for content in contentList:
                    words = []
                    sentence = content["stepText"].replace("  ", " ")
                    sentence = sentence.lower().replace(".", " ")
                    sentence = sentence.replace("  ", " ")
                    sentences = sentence.split(" ")
                    for i, word in enumerate(sentences):
                        if word in wordsObject:
                            wordsObject[word] += 1
                        else:
                            wordsObject[word] = 1
            except:
                pass

wordsObject = sorted(wordsObject.items(), key=lambda x: x[1], reverse=True)

f = open("words.txt", "w+")
for x in wordsObject:
    f.write(x[0] + ":" + str(x[1]) + "\n")
f.close()
