use agg;
db.inventory.drop();
db.inventory.insert({'name':"Polo Shirt", 'sizes':["Small", "Medium", "Large"], 'colors':['navy', 'white', 'orange', 'red']})
db.inventory.insert({'name':"T-Shirt", 'sizes':["Small", "Medium", "Large", "X-Large"], 'colors':['navy', "black",  'orange', 'red']})
db.inventory.insert({'name':"Chino Pants", 'sizes':["32x32", "31x30", "36x32"], 'colors':['navy', 'white', 'orange', 'violet']})
db.inventory.aggregate([
    {$unwind: "$sizes"},
    {$unwind: "$colors"},
//    {
//        "_id" : ObjectId("5128c517ed241b4dede3776a"),
//        "name" : "Polo Shirt",
//        "sizes" : "Small",
//        "colors" : "navy"
//    },
    /* create the color array */
    {$group: 
     {
	'_id': {name:"$name",size:"$sizes"},
	 'colors': {$push: "$colors"},
     }
    },

//    {
//        "sizes" : [
//            "Medium",
//            "Large",
//            "Small"
//        ],
//        "name" : "Polo Shirt",
//        "colors" : [
//            "navy",
//            "white",
//            "orange",
//            "red"
//        ]
//    },
//    {
//        "sizes" : [
//            "Medium",
//            "Small",
//            "X-Large",
//            "Large"
//        ],
//        "name" : "T-Shirt",
//        "colors" : [
//            "navy",
//            "black",
//            "orange",
//            "red"
//        ]
//    },

    /* create the size array */
    {$group: 
     {
	'_id': {'name':"$_id.name",
		'colors' : "$colors"},
	 'sizes': {$push: "$_id.size"}
     }
    },
    /* reshape for beauty */
    {$project: 
     {
	 _id:0,
	 "name":"$_id.name",
	 "sizes":1,
	 "colors": "$_id.colors"
     }
    }
])

