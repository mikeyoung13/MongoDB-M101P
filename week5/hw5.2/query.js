use hw5-2
db.zips.aggregate([
    {
        $match : {$or:[{state:"CT"},{state:"NJ"}]}
    },
    {
        $group : {
            _id:"$city",
            ave_pop:{$avg:"$pop"}
        }
    },
    {
        $match : {ave_pop:{$gt:25000}}
    }

])