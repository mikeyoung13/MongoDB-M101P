import bottle

import pymongo
import cgi
import re
import datetime
import random
import hmac
import user
import sys

connection_string = "mongodb://localhost"


# inserts the blog entry and returns a permalink for the entry
def insert_entry(title, post, tags_array, author):
    print "inserting blog entry", title, post

    connection = pymongo.Connection(connection_string, safe=True)

    db = connection.blog
    posts = db.posts

    exp = re.compile('\W') # match anything not alphanumeric
    whitespace = re.compile('\s')
    temp_title = whitespace.sub("_",title)
    permalink = exp.sub('', temp_title)

    post = {"title": title, 
            "author": author,
            "body": post, 
            "permalink":permalink, 
            "tags": tags_array, 
            "date": datetime.datetime.utcnow()}

    try:

        posts.insert(post)
        print "Inserting the post"

    except:
        print "Error inserting post"
        print "Unexpected error:", sys.exc_info()[0]

    return permalink
    

@bottle.route('/')
def blog_index():
    connection = pymongo.Connection(connection_string, safe=True)
    db = connection.blog
    posts = db.posts

    username = login_check()  # see if user is logged in

    cursor = posts.find().sort('date', direction=-1).limit(10)
    l=[]
    
    for post in cursor:
        post['date'] = post['date'].strftime("%A, %B %d %Y at %I:%M%p") # fix up date
        if ('tags' not in post):
            post['tags'] = [] # fill it in if its not there already
        if ('comments' not in post):
            post['comments'] = []
            
        l.append({'title':post['title'], 'body':post['body'], 'post_date':post['date'], 
                  'permalink':post['permalink'], 
                  'tags':post['tags'],
                  'author':post['author'],
                  'comments':post['comments']})


    return bottle.template('blog_template', dict(myposts=l,username=username))

@bottle.route('/tag/<tag>')
def posts_by_tag(tag="notfound"):
    connection = pymongo.Connection(connection_string, safe=True)
    db = connection.blog
    posts = db.posts

    username = login_check()  # see if user is logged in

    tag = cgi.escape(tag)
    cursor = posts.find({'tags':tag}).sort('date', direction=-1).limit(10)
    l=[]
    
    for post in cursor:
        post['date'] = post['date'].strftime("%A, %B %d %Y at %I:%M%p") # fix up date
        if ('tags' not in post):
            post['tags'] = [] # fill it in if its not there already
        if ('comments' not in post):
            post['comments'] = []
            
        l.append({'title':post['title'], 'body':post['body'], 'post_date':post['date'], 
                  'permalink':post['permalink'], 
                  'tags':post['tags'],
                  'author':post['author'],
                  'comments':post['comments']})

    return bottle.template('blog_template', dict(myposts=l,username=username))


# gets called both for regular requests and json requests
@bottle.get("/post/<permalink>")
def show_post(permalink="notfound"):
    connection = pymongo.Connection(connection_string, safe=True)
    db = connection.blog
    posts = db.posts

    username = login_check()  # see if user is logged in
    permalink = cgi.escape(permalink)

    # determine if its a json request
    path_re = re.compile(r"^([^\.]+).json$")
    
    print "about to query on permalink = ", permalink
    post = posts.find_one({'permalink':permalink})

    if post == None:
        bottle.redirect("/post_not_found")
    
    print "date of entry is ", post['date']

    # fix up date
    post['date'] = post['date'].strftime("%A, %B %d %Y at %I:%M%p")

    # init comment form fields for additional comment
    comment = {}
    comment['name'] = ""
    comment['email'] = ""
    comment['body'] = ""

    return bottle.template("entry_template", dict(post=post, username=username, errors="", comment=comment))


# used to process a comment on a blog post
@bottle.post('/newcomment')
def post_newcomment():
    name = bottle.request.forms.get("commentName")
    email = bottle.request.forms.get("commentEmail")
    body = bottle.request.forms.get("commentBody")
    permalink = bottle.request.forms.get("permalink")


    # look up the post in question
    connection = pymongo.Connection(connection_string, safe=True)
    db = connection.blog
    posts = db.posts

    username = login_check()  # see if user is logged in
    permalink = cgi.escape(permalink)

    post = posts.find_one({'permalink':permalink})
    # if post not found, redirct to post not found error
    if post == None:
        bottle.redirect("/post_not_found")

    # if values not good, redirect to view with errors
    errors=""
    if (name == "" or body == ""):

        # fix up date
        post['date'] = post['date'].strftime("%A, %B %d %Y at %I:%M%p")

        # init comment
        comment = {}
        comment['name'] = name
        comment['email'] = email
        comment['body'] = body

        errors="Post must contain your name and an actual comment."
        print "newcomment: comment contained error..returning form with errors"
        return bottle.template("entry_template", dict(post=post, username=username, errors=errors, comment=comment))

    else:

        # it all looks good, insert the comment into the blog post and redirect back to the post viewer
        comment = {}
        comment['author'] = name
        if (email != ""):
            comment['email'] = email
        comment['body'] = body

        try:
            last_error = posts.update({'permalink':permalink}, {'$push':{'comments':comment}}, upsert=False, manipulate=False, safe=True)

            print "about to update a blog post with a comment"
            
            #print "num documents updated" + last_error['n']
        except:
            print "Could not update the collection, error"
            print "Unexpected error:", sys.exc_info()[0]



        print "newcomment: added the comment....redirecting to post"

        bottle.redirect("/post/"+permalink)

        
    
@bottle.get("/post_not_found")
def post_not_found():
    return "Sorry, post not found"


# how new posts are made. this shows the initial page with the form
@bottle.get('/newpost')
def get_newpost():

    username = login_check()  # see if user is logged in
    if (username == None):
        bottle.redirect("/login")        

    return bottle.template("newpost_template", dict(subject="", body="",errors="", tags="", username=username))

# extracts the tag from the tags form element. an experience python programmer could do this in  fewer lines, no doubt
def extract_tags(tags):

    whitespace = re.compile('\s')

    nowhite = whitespace.sub("",tags)
    tags_array = nowhite.split(',')

    # let's clean it up
    cleaned = []
    for tag in tags_array:
        if (tag not in cleaned and tag != ""):
            cleaned.append(tag)

    return cleaned

# put handler for setting up a new post
@bottle.post('/newpost')
def post_newpost():
    title = bottle.request.forms.get("subject")
    post = bottle.request.forms.get("body")
    tags = bottle.request.forms.get("tags")

    username = login_check()  # see if user is logged in
    if (username is None):
        bottle.redirect("/login")        
    
    if (title == "" or post == ""):
        errors="Post must contain a title and blog entry"
        return bottle.template("newpost_template", dict(subject=cgi.escape(title, quote=True), username=username,
                                                 body=cgi.escape(post, quote=True), tags=tags, errors=errors))

    # extract tags
    tags = cgi.escape(tags)
    tags_array = extract_tags(tags)
    
    # looks like a good entry, insert it escaped
    escaped_post = cgi.escape(post, quote=True)

    # substitute some <p> for the paragraph breaks
    newline = re.compile('\r?\n')
    formatted_post = newline.sub("<p>",escaped_post)
    
    permalink=insert_entry(title, formatted_post, tags_array, username)

    # now bottle.redirect to the blog permalink
    bottle.redirect("/post/" + permalink)

# displays the initial blog signup form
@bottle.get('/signup')
def present_signup():
    return bottle.template("signup", 
                           dict(username="", password="", 
                                password_error="", 
                                email="", username_error="", email_error="",
                                verify_error =""))

# displays the initial blog login form
@bottle.get('/login')
def present_login():
    return bottle.template("login", 
                           dict(username="", password="", 
                                login_error=""))

# handles a login request
@bottle.post('/login')
def process_login():

    connection = pymongo.Connection(connection_string, safe=True)

    username = bottle.request.forms.get("username")
    password = bottle.request.forms.get("password")

    print "user submitted ", username, "pass ", password

    userRecord = {}
    if (user.validate_login(connection, username, password, userRecord)):
        session_id = user.start_session(connection, username)
        if (session_id == -1):
            bottle.redirect("/internal_error")

        cookie = user.make_secure_val(session_id)

        # Warning, if you are running into a problem whereby the cookie being set here is 
        # not getting set on the redirct, you are probably using the experimental version of bottle (.12). 
        # revert to .11 to solve the problem.
        bottle.response.set_cookie("session", cookie)
        
        bottle.redirect("/welcome")

    else:
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


