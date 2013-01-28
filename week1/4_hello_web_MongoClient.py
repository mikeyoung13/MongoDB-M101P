import bottle
#import pymongo

@bottle.route('/')
def index():
    # switch from Connection to MongoClient
    from pymongo import MongoClient
    connection = MongoClient('localhost',27017)
    db = connection.test
    names = db.names
    item = names.find_one()
    return '<b>Hello %s!</b>' % item['name']

bottle.run(host='localhost', port=8082)
# test URL: http://localhost:8082/
