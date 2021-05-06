import mongoUtil from '$lib/db'

export async function post({ body }) {

  let query = []
  let match = {}

  if (body && body.documentId) match.texteLegislatifRef = body.documentId

  query = [
    {
      '$match': match
    },
    {
      '$group': {
        '_id': {
          'statut': '$statut',
          'groupe': '$groupe'
        },
        'count': {
          '$sum': '$count'
        }
      }
    }, {
      '$group': {
        '_id': '$_id.groupe',
        'agg': {
          '$push': {
            'k': '$_id.statut',
            'v': '$count'
          }
        },
        'count': {
          '$sum': '$count'
        }
      }
    }, {
      '$project': {
        '_id': 0,
        'groupe': '$_id',
        'res': {
          '$arrayToObject': '$agg'
        },
        'count': 1
      }
    }, {
      '$sort': {
        'count': -1
      }
    }
  ]

  return {
    body: await mongoUtil.db.collection('amend-group-statut')
      .aggregate(query)
      .toArray()
      .then(res => res
        .map(({ groupe, res, count }) => ({ groupe, ...res }))
      )
  }
}