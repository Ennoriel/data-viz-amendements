var MongoUtil = require('./mongo.util');
ObjectID = require('mongodb').ObjectID

class Amendements {
  
  async get(_id) {
    return await MongoUtil.db.collection('amendements').find({_id: ObjectID(_id)}).toArray();
  }

  async agg() {
    return await MongoUtil.db.collection('amendements').aggregate(
      [
        {
          '$facet': {
            'dp': [
              {
                '$sortByCount': '$auteur'
              }
            ]
          }
        }, {
          '$unwind': {
            'path': '$dp'
          }
        }, {
          '$replaceRoot': {
            'newRoot': '$dp'
          }
        }, 
        // {
        //   '$match': {
        //     'count': {
        //       '$gte': 10
        //     }
        //   }
        // }
      ]
    ).toArray();
  }
}
module.exports = new Amendements();