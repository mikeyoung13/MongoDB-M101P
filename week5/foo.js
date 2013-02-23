db.fun.aggregate([
    {$match:{a:0}},
    {$sort:{c:-1}}, 
    {$group:{_id:"$a", c:{$first:"$c"}}}
])

