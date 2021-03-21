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
      ]
    ).toArray();
  }

  async projectAuteurSort(documentId) {

    let query = []
    
    if (documentId) {
      query.push({
        $match: {
          texteLegislatifRef: documentId
        }
      })
    }

    query.push(...[
      {
        $match: {
          isDepute: true
        }
      },
      {
        '$group': {
          '_id': {
            'sort': '$sort', 
            'auteur': '$auteur'
          }, 
          'count': {
            '$sum': 1
          }
        }
      }, {
        '$project': {
          '_id': 0, 
          'sort': '$_id.sort', 
          'auteur': '$_id.auteur', 
          'count': 1
        }
      }, {
        '$group': {
          '_id': '$auteur', 
          'statuts': {
            '$push': {
              'k': '$sort', 
              'v': '$count'
            }
          },
          count: {
            $sum: "$count"
          }
        }
      }, {
        '$project': {
          '_id': 0, 
          'auteur': '$_id', 
          count: 1,
          'statuts': {
            '$arrayToObject': '$statuts'
          }
        }
      },
      {
        $lookup: {
          from: 'acteurs',
          localField: 'auteur',
          foreignField: 'uid',
          as: 'test'
        }
      },
      {
        $unwind: {
          path: '$test'
        }
      },
      {
        $sort: {
          count: -1
        }
      },
      {
        '$limit': 3000  
      }
    ])

    let res = await MongoUtil.db.collection('amendements').aggregate(query).toArray();
    return res.map(({auteur, test, statuts}) => ({auteur: test && `${test.nom} ${test.prenom}` || auteur, ...statuts}))
  }

  async projectDayMonth(year, documentId) {
    
    let query = []

    if (documentId) {
      query.push({
        $match: {
          texteLegislatifRef: documentId
        }
      })
    }

    query.push(...[
      {
        '$group': {
          '_id': {
            'day': {  '$dayOfMonth': '$dateDepot' }, 
            'month': { '$month': '$dateDepot' },
            'year': '$yearDepot'
          }, 
          'count': {
            '$sum': 1
          }
        }
      },
      {
        $group: {
          _id: "$_id.year",
          data: {
            "$push": {
              month: "$_id.month",
              day: "$_id.day",
              count: "$count"
            }
          }
        }
      }
    ])

    return await MongoUtil.db.collection('amendements').aggregate(query).toArray();
  }
}
module.exports = new Amendements();