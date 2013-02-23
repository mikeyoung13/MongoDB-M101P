use blog
db.posts.aggregate([

    {$match:
        {
            "_id" : ObjectId("50ab0f8bbcf1bfe2536dc3f8")
        }
    },

    {$project:
        {
            _id:0,
            'comments.author' : 1
        }
    },

    {$unwind:"$comments"}
])

