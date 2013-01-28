import pymongo

connection = pymongo.Connection("localhost", 27017)
db = connection.test 

names = db.names

item = names.find_one()

print item['name']
