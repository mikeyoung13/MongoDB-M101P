import cgi
import re
import hmac
import random
import string
import hashlib
import pymongo
import bson
import sys

# makes a little salt
def make_salt():
    salt = ""
    for i in range(5):
        salt = salt + random.choice(string.ascii_letters)
    return salt


# implement the function make_pw_hash(name, pw) that returns a hashed password 
# of the format: 
# HASH(pw + salt),salt
# use sha256

def make_pw_hash(pw,salt=None):
    if (salt == None):
        salt = make_salt();
    return hashlib.sha256(pw + salt).hexdigest()+","+ salt


# validates that the user information is valid, return True of False 
# and fills in the error codes
def validate_signup(username, password, verify, email, errors):
    USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
    PASS_RE = re.compile(r"^.{3,20}$")
    EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")

    errors['username_error']  = ""
    errors['password_error'] = ""
    errors['verify_error'] = ""
    errors['email_error'] = ""
    

    if not USER_RE.match(username):
        errors['username_error']  = "invalid username. try just letters and numbers"
        return False

    if not PASS_RE.match(password):
        errors['password_error'] = "invalid password."
        return False
    if password != verify:
        errors['verify_error'] = "password must match"
        return False
    if email != "":
        if not EMAIL_RE.match(email):
            errors['email_error'] = "invalid email address"
            return False
    return True

# validates the login, returns True if it's a valid user login. false otherwise
def validate_login(connection, username, password, user_record):
    db = connection.blog
    users = db.users

    try:
        user = users.find_one({'_id':username})
    except:
        print "Unable to query database for user"


    if user == None:
        print "User not in database"
        return False
    
    salt = user['password'].split(',')[1]


    if (user['password'] != make_pw_hash(password,salt)):
        print "user password is not a match"
        return False

    # looks good

    for key in user:
        user_record[key] = user[key] # perform a copy

    return True

# will start a new session id by adding a new document to the sessions collection
def start_session(connection, username):
    db = connection.blog
    sessions = db.sessions


    session = {'username':username}

    try:
        sessions.insert(session, safe=True)
    except:
        print "Unexpected error on start_session:", sys.exc_info()[0]
        return -1

    return str(session['_id'])

# will send a new user session by deleting from sessions table
def end_session(connection, session_id):
    db = connection.blog
    sessions = db.sessions

    # this may fail because the string may not be a valid bson objectid
    try:
        id = bson.objectid.ObjectId(session_id)
        sessions.remove({'_id':id})
    except:
        
        return



# if there is a valid session, it is returned
def get_session(connection, session_id):

    db = connection.blog
    sessions = db.sessions

    # this may fail because the string may not be a valid bson objectid
    try:
        id = bson.objectid.ObjectId(session_id)
    except:
        print "bad sessionid passed in"
        return None

    session = sessions.find_one({'_id':id})

    print "returning a session or none"
    return session



# creates a new user in the database
def newuser(connection, username, password, email):
    password_hash = make_pw_hash(password)

    user = {'_id':username, 'password':password_hash}
    if (email != ""):
        user['email'] = email

    db = connection.blog
    users = db.users

    try:
        db.users.insert(user, safe=True)
    except pymongo.errors.OperationFailure:
        print "oops, mongo error"
        return False
    except pymongo.errors.DuplicateKeyError as e:
        print "oops, username is already taken"
        return False

    return True

def uid_to_username(connection, uid):
    db = connection.blog
    users = db.users
    
    user = users.find_one({'uid':int(uid)})

    return user['username']
    

# Implement the hash_str function to use HMAC and our SECRET instead of md5
SECRET = 'verysecret'
def hash_str(s):
    return hmac.new(SECRET, s).hexdigest()

# call this to hash a cookie value
def make_secure_val(s):
    return "%s|%s" % (s, hash_str(s))

# call this to make sure that the cookie is still secure
def check_secure_val(h):
    val = h.split('|')[0]
    if h == make_secure_val(val):
        return val
