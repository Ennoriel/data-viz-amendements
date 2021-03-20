var MongoUtil = require('./mongo.util');

class Documents {
  
  async get() {
    return await MongoUtil.db.collection('amendements').aggregate(
      [
        { '$facet': { 'doc': [ { '$sortByCount': '$texteLegislatifRef' } ] }},
        { '$unwind': { 'path': '$doc' }},
        { '$limit': 100},
        { '$lookup': { 'from': 'documents', 'localField': 'doc._id', 'foreignField': 'uid', 'as': 'doc' }},
        { '$unwind': { 'path': '$doc' }},
        { '$replaceRoot': { 'newRoot': '$doc' }}
      ]
    ).toArray();
  }
}

module.exports = new Documents();