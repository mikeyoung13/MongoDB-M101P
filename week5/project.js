use school2
db.students.aggregate([
    {$match: {'student_id':{$lt:50}}},
    {$project: {'class': {$add:["$class_id", "$class_id"]}}}])
