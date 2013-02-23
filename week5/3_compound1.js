use agg
db.products.aggregate([
    {$group:
     {
	 _id: {
	     "maker":"$manufacturer", 
	     "category" : "$category"},
	 avg_price:{$avg:"$price"}
     }
    }
])


