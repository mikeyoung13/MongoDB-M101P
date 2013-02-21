use agg;
db.people.drop();
db.people.insert({_id: "Barack Obama", likes:['social justice', 'health care', 'taxes']})
db.people.insert({_id: "Mitt Romney", likes:['a balanced budget', 'corporations', 'binders full of women']})
db.people.aggregate([{$unwind:"$likes"}])
