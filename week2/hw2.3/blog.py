import bottle

import pymongo
import cgi
import re
import datetime
import random
import hmac
import user
import json
import sys

connection_string = "mongodb://localhost"

@bottle.route('/')
def blog_index():

    return 'This is a place holder for the blog'


@bottle.get('/signup')
def present_signup():
    return bottle.template("signup", 
                           dict(username="", password="", 
                                password_error="", 
                                email="", username_error="", email_error="",
                                verify_error =""))

@bottle.get('/login')
def present_login():
    return bottle.template("login", 
                           dict(username="", password="", 
                                login_error=""))

@bottle.post('/login')
def process_login():

    connection = pymongo.Connection(connection_string, safe=True)

    username = bottle.request.forms.get("username")
    password = bottle.request.forms.get("password")

    userRecord = {}
    if (user.validate_login(connection, username, password, userRecord)):
        # looks good. start a new session
        session_id = user.start_session(connection, username)
        if (session_id == -1):
            bottle.redirect("/internal_error")

        cookie = user.make_secure_val(session_id)
        # send the cookie back to the user
        bottle.response.set_cookie("session", cookie)
        
        # full round trip here.
        
        bottle.redirect("/welcome")

    else:
        # not a valid login
        return bottle.template("login", 
                           dict(username=cgi.escape(username), password="", 
                                login_error="Invalid Login"))


@bottle.get('/internal_error')
@bottle.view('error_template')
def present_internal_error():
    return ({error:"System has encountered a DB error"})


@bottle.get('/logout')
def process_logout():

    connection = pymongo.Connection(connection_string, safe=True)

    cookie = bottle.request.get_cookie("session")

    if (cookie == None):
        print "no cookie..."
        bottle.redirect("/signup")

    else:
        session_id = user.check_secure_val(cookie)

        if (session_id == None):
            print "no secure session_id"
            bottle.redirect("/signup")
            
        else:
            # remove the session

            user.end_session(connection, session_id)

            print "clearing the cookie"

            bottle.response.set_cookie("session","")


            bottle.redirect("/signup")


@bottle.post('/signup')
def process_signup():

    connection = pymongo.Connection(connection_string, safe=True)

    email = bottle.request.forms.get("email")
    username = bottle.request.forms.get("username")
    password = bottle.request.forms.get("password")
    verify = bottle.request.forms.get("verify")

    # set these up in case we have an error case
    errors = {'username':cgi.escape(username), 'email':cgi.escape(email)}
    if (user.validate_signup(username, password, verify, email, errors)):
        if (not user.newuser(connection, username, password, email)):
            # this was a duplicate
            errors['username_error'] = "Username already in use. Please choose another"
            return bottle.template("signup", errors)
            
        session_id = user.start_session(connection, username)
        print session_id
        cookie= user.make_secure_val(session_id)
        bottle.response.set_cookie("session",cookie)
        bottle.redirect("/welcome")
    else:
        print "user did not validate"
        return bottle.template("signup", errors)


# will check if the user is logged in and if so, return the username. otherwise, it returns None
def login_check():
    connection = pymongo.Connection(connection_string, safe=True)
    cookie = bottle.request.get_cookie("session")

    if (cookie == None):
        print "no cookie..."
        return None

    else:
        session_id = user.check_secure_val(cookie)

        if (session_id == None):
            print "no secure session_id"
            return None
            
        else:
            # look up username record
            session = user.get_session(connection, session_id)
            if (session == None):
                return None

    return session['username']


    
@bottle.get("/welcome")
def present_welcome():
    # check for a cookie, if present, then extract value

    username = login_check()
    if (username == None):
        print "welcome: can't identify user...redirecting to signup"
        bottle.redirect("/signup")

    return bottle.template("welcome", {'username':username})        



bottle.debug(True)
bottle.run(host='localhost', port=8082)


