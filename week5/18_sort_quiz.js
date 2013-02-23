use agg
db.zips.aggregate([
    {$sort:
     {
	 state:1,city:1
     }
    }
])


