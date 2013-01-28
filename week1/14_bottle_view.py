import bottle

@bottle.route('/')
def home_page():
    mythings = ['apple','orange','banana','peach']

    # one way:
    #return bottle.template('14_bottle_view', username="Mike", things=mythings)

    # another way:
    return bottle.template('14_bottle_view',{'username':'Mike2',
                                             'things' : mythings})


bottle.debug(True)
bottle.run(host='localhost',port=8080)

#URL: http://localhost:8080/

