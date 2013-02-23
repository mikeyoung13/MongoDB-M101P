use blog
db.posts.aggregate([

    {$match:
        {
            "_id" : ObjectId("50ab0f8bbcf1bfe2536dc3f8")
        }
    },

    {$project:
        {
            //_id:0,
            author: "$comments.author"
        }
    },

    {$unwind:"$author"},

    {$group:
        {
            _id:"$author",
            numComments:{$sum:1}
        }
    },

    {$sort:
        {
            numComments:-1
        }
    },

    {$limit: 2}

])

