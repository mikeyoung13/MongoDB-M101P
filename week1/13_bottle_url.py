import bottle

@bottle.route('/')
def home_page():
    return "Hello World\n"

@bottle.route('/testpage')
def test_page():
    return "this is a test page"

bottle.debug(True)
bottle.run(host='localhost',port=8080)

#URL: http://localhost:8080/
#URL: http://localhost:8080/testpage
#curl -i http://localhost:8080/
