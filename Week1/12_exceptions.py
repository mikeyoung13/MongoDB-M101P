import sys

try:
    print 5/0
except:
    # note comma requires to concat str and object
    print "Exception " , sys.exc_info()[0]
    print "Exception " , sys.exc_info()[1]
    print "Exception " , sys.exc_info()[2]

print "but life goes on"
