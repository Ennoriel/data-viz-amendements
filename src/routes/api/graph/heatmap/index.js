import mongoUtil from '$lib/db'

export async function post({ body }) {

  let query = []
  let match = {}

  if (body && body.documentId) match.texteLegislatifRef = body.documentId
  if (body && body.acteurId) match.auteur = body.acteurId

  query.push(...[{
    '$match': match
  },
  {
    '$group': {
      '_id': {
        'day': '$depot.day',
        'month': '$depot.month',
        'year': '$depot.year'
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

  return {
    body: await mongoUtil.db.collection('amendements').aggregate(query).toArray()
  }
}