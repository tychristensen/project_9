import json

with open('business.json', encoding='utf8') as json_file:
    entry = json_file.readline()
    obj = json.loads(entry)
    while entry:
        if(str(obj['categories']).find('Bakeries') != -1):
            print(obj['name'])
        entry = json_file.readline()
        obj = json.loads(entry)
