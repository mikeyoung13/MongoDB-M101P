
import pymongo
import sys
import traceback

# establish a connection to the database
connection = pymongo.Connection("mongodb://localhost", safe=True)

# get a handle to the school database
db=connection.school
students = db.students


def drop_low_score():

    print "dropping low score..."

    query = {}

    try:
        cursor = students.find(query)

        for doc in cursor:
            lowScore = 101.0
            for scores in doc['scores']:
                scoreType = scores['type']
                if (scoreType == 'homework'):
                    score = scores['score']
                    if (score < lowScore):
                        lowScore = score


                print scores['type'],scores['score']

            print 'low score is:',lowScore
            doc['scores'].remove({'type':'homework','score':lowScore})
            print doc['scores']

            students.update({'_id':doc['_id']},{'$set':{'scores':doc['scores']}})


    except:
#        print "Unexpected error:", sys.exc_info()[0],sys.exc_info()[1],sys.exc_info()[2]
        for frame in traceback.extract_tb(sys.exc_info()[2]):
            fname,lineno,fn,text = frame
            print "Error in %s on line %d" % (fname, lineno)
            print sys.exc_info()[0],sys.exc_info()[1]

#    for doc in cursor:
#        print doc
        


drop_low_score()

