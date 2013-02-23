use agg
db.zips.aggregate([
    {$match:
     {
	    pop:{$gt:100000}
     }
    }
])


