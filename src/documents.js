var MongoUtil = require('./mongo.util');

class Documents {
  
  async get() {
    return MongoUtil.db.collection('amendements').aggregate(
      [
        { '$facet': { 'stats': [ { '$sortByCount': '$texteLegislatifRef' } ] }},
        { '$unwind': { 'path': '$stats' }},
        { '$limit': 100},
        { '$lookup': { 'from': 'documents', 'localField': 'stats._id', 'foreignField': 'uid', 'as': 'doc' }},
        { '$addFields': { 'doc.count': '$stats.count' }},
        { '$unwind': { 'path': '$doc' }},
        { '$replaceRoot': { 'newRoot': '$doc' }}
      ]
    ).toArray();
  }
}

module.exports = new Documents();