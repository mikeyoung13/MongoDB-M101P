use agg
db.zips.aggregate([
    {$match:
     {
	 state:"NY"
     }
    },
    {$group:
     {
	 _id: "$city",
	 population: {$sum:"$pop"},
     state: {$addToSet: "$state"}
     }
    },
    {$project:
     {
	 _id: 0,
	 city: "$_id",
	 population: 1,
     state: 1
     }
    },
    {$sort:
     {
	 population:-1
     }
    },
    {$skip: 10},
    {$limit: 5}
])


