use hw5-2
db.zips.aggregate([
    {
        $match : {$or:[{state:"CA"},{state:"NY"}]}
    },
    {
        $group : {
            _id:
                {city:"$city",
                 state: "$state"},
            pop:{$sum:"$pop"}
        }
    },
    {
        $match : {pop:{$gt:25000}}
    },
    {
        $group : {
            _id:null,
            ave_pop:{$avg:"$pop"}
        }
    }

])