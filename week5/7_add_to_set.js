
use agg
db.products.aggregate([{"$group":{_id: "$manufacturer", "categories": {"$addToSet":"$category"}}}])
