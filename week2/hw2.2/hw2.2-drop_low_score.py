
import pymongo
import sys

# establish a connection to the database
connection = pymongo.Connection("mongodb://localhost", safe=True)

# get a handle to the school database
db=connection.students
grades = db.grades


def drop_low_score():

    print "dropping low score..."

    query = {'type':'homework'}

    try:
        cursor = grades.find(query)
        cursor = cursor.sort([('student_id',pymongo.ASCENDING),('score',pymongo.DESCENDING)])

        lastStudentID = -1
        lastObjectID = -1;

        for doc in cursor:
            currentStudentID = doc['student_id']
            if (currentStudentID != lastStudentID):
                if (lastStudentID != -1):
                    print 'delete',lastStudentID, currentStudentID, lastObjectID, doc['score']
                    db.grades.remove({'_id':lastObjectID})
                    # delete score
                lastStudentID = currentStudentID
            else:
                print 'same student', doc['score']
            lastObjectID =  doc['_id'];



    except:
        print "Unexpected error:", sys.exc_info()[0]

#    for doc in cursor:
#        print doc
        


drop_low_score()

