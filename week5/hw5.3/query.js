use hw5-3
db.grades.aggregate([
//    {
//        $match: {
//             _id:ObjectId("50b59cd75bed76f46522c34e")
//        }
//    }
//    ,
    {
        $unwind: "$scores"
    }
    ,
    {
        $match: {$or:[{"scores.type":"quiz"},{"scores.type":"exam"}]}
    }

//      $match : {$or:[{state:"CA"},{state:"NY"}]}

//    ,
//    {
//        $group : {
//            _id: "$scores.type",
//            count:{$sum:1}
//        }
//    }

])