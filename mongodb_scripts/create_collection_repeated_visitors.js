var col1 = db.processed_reviews.aggregate([
    { $group: { _id: { uid: "$uid", attraction: "$attraction"},
               count: { $sum: 1 } } },
   { $match: { count: { $gt: 1 } } },
   { $project: { _id: 0,
                 uid: "$_id.uid",
                 attraction: "$_id.attraction",
                 count: 1}},
   { $out: "single_user_multiple_reviews"}
])

var col2 = db.single_user_multiple_reviews.aggregate([
    { $match: { attraction: {$eq: "Singapore Zoo"},
                uid : {$ne: ""} } },
    { $sort : { count : -1 } },
    { $lookup: {
          from: "processed_reviews",
          localField: "uid",
          foreignField: "uid",
          as: "reviews"
    }},
    { $project: {
          "_id": 0,
           "uid": 1,
           "attraction": 1,
           "count": 1,
           "reviews": { $filter: {
                        input: "$reviews",
                        as: "review",
                        cond: { $eq: ["$$review.attraction", "Singapore Zoo"]}
                     }}
    }},
    { $out: "repeated_visitors_singapore_zoo"}
])

var col3 = db.single_user_multiple_reviews.aggregate([
    { $match: { attraction: {$eq: "River Safari"},
                uid : {$ne: ""} } },
    { $sort : { count : -1 } },
    { $lookup: {
          from: "processed_reviews",
          localField: "uid",
          foreignField: "uid",
          as: "reviews"
    }},
    { $project: {
          "_id": 0,
           "uid": 1,
           "attraction": 1,
           "count": 1,
           "reviews": { $filter: {
                        input: "$reviews",
                        as: "review",
                        cond: { $eq: ["$$review.attraction", "River Safari"]}
                     }}
    }},
    { $out: "repeated_visitors_river_safari"}
])

var col4 = db.single_user_multiple_reviews.aggregate([
    { $match: { attraction: {$eq: "Night Safari"},
                uid : {$ne: ""} } },
    { $sort : { count : -1 } },
    { $lookup: {
          from: "processed_reviews",
          localField: "uid",
          foreignField: "uid",
          as: "reviews"
    }},
    { $project: {
          "_id": 0,
           "uid": 1,
           "attraction": 1,
           "count": 1,
           "reviews": { $filter: {
                        input: "$reviews",
                        as: "review",
                        cond: { $eq: ["$$review.attraction", "Night Safari"]}
                     }}
    }},
    { $out: "repeated_visitors_night_safari"}
])
    
print("Size of db.repeated_visitors_singapore_zoo is " + db.repeated_visitors_singapore_zoo.find().count() + "\n" + 
      "Size of db.repeated_visitors_singapore_zoo is " + db.repeated_visitors_river_safari.find().count() + "\n" +
      "Size of db.repeated_visitors_singapore_zoo is " + db.repeated_visitors_night_safari.find().count())
