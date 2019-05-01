import json

with open('business.json', encoding='utf8', errors='ignore') as json_file:
    entry = json_file.readline()
    obj = json.loads(entry)
    count = 0
    while entry:
        if(str(obj['categories']).find('Bakeries') != -1 and str(obj['city']).find('Denver') != -1):
            print(obj['name'])
        entry = json_file.readline()
        obj = json.loads(entry)
