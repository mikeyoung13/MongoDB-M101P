use agg;
db.zips.aggregate([
    {'$match':{'state':'CA'}},
    {'$group':
     {
	_id: "$city",
	zips: {$push:"$_id"}
     }
    },
    {"$unwind":"$zips"}
]);

