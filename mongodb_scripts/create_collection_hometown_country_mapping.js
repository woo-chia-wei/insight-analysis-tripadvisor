db.raw_users.aggregate([
    {
      $lookup:
        {
          from: "processed_users",
          localField: "uid",
          foreignField: "uid",
          as: "output"
        }
   },
   {
       $project:
       {
           hometown: 1,
           user: {$arrayElemAt: ['$output', 0]}
       }
   },
   {
       $project:
        {
            hometown: 1,
            country: "$user.country"
        }
   },
   {
       $out: "hometown_country_mapping"
   }   
])