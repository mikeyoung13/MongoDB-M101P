use school2
db.students.aggregate([
    {$match: {'student_id':{"$lt":1000}}},
    {$unwind: "$scores"},
    {$group: {_id:
	     {"class":"$class_id",
	      "student_id":"$student_id"},
	     "average":{$avg:"$scores.score"}}},
    {$group: {_id:{'class':"$_id.class"}, class_average:{$avg:"$average"}}},
    {$sort: {"_id.student_id":1, "_id.class":1}}])
	
