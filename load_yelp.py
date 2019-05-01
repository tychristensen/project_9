import json
import getpass
import pg8000
import pprint

user = input('Username: ')
secret = getpass.getpass()
db = pg8000.connect(user=user, password=secret, host='flowers.mines.edu', database='csci403')
cursor = db.cursor()
db.autocommit = True

cursor.execute('DROP TABLE IF EXISTS business')
cursor.execute('CREATE TABLE business (id serial, name text, address text, service text, latitude float, longitude float, num_reviews int, stars float)')

with open('business.json', encoding='utf8', errors='ignore') as json_file:
    entry = json_file.readline()
    obj = json.loads(entry)
    while entry:
        entry = json_file.readline()
        obj = json.loads(entry)
        category = str(obj['categories'])
        if ('Bakeries' in category or 'Bars' in category):

            if 'Bakeries' in category:
                service = 'bakery'
            else:
                service = 'bar'

            print(obj['name'])
            query = "INSERT INTO business (name, address, service, latitude, longitude, num_reviews, stars)"
            query += " VALUES ('" + str(obj['name']).replace("'", "") + "', '"
            query += str(obj['address']).replace("'", "") + "', '"
            query += str(service) + "', '"
            query += str(obj['latitude']) + "', '"
            query += str(obj['longitude']) + "', '"
            query += str(obj['review_count']) + "', '"
            query += str(obj['stars']) + "')"
            print(query)
            cursor.execute(query)
