use hw5-3
db.grades.aggregate([
    {
        $unwind: "$scores"
    }
    ,
    {
        $match: {$or:[{"scores.type":"homework"},{"scores.type":"exam"}]}
    }
    ,
    {
        $group : {
            _id: {student_id:"$student_id",
                  class_id: "$class_id"}
            ,
            student_ave:{$avg:"$scores.score"}
        }
    }
    ,
    {
        $group : {
            _id: {'class': "$_id.class_id"},
            class_average:{$avg:"$student_ave"}
        }
    }
    ,
    {$sort:
        {"class_average":-1}
    }
    ,
    {$limit: 1}

])