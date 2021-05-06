import mongoUtil from '$lib/db'

export async function post({ body }) {

  let query = []
  let match = {}

  if (body && body.documentIds) match.texteLegislatifRef = { $in: body.documentIds }
  if (body && body.acteurIds) match.auteur = { $in: body.acteurIds }

  query.push(...[{
    $match: match
  },
  {
    $lookup: {
      from: 'acteurs',
      localField: 'auteur',
      foreignField: 'uid',
      as: 'auteurObj'
    }
  },
  {
    $unwind: {
      path: "$auteurObj"
    }
  },
  {
    $facet: {
      t: [{
        $group: {
          _id: {
            texteLegislatifRef: "$texteLegislatifRef",
            auteur: { $concat: ["$auteurObj.nom", " ", "$auteurObj.prenom"] }
          },
          count: { $sum: 1 }
        }
      }],
      u: [{
        $group: {
          _id: {
            texteLegislatifRef: "$texteLegislatifRef",
            statut: "$statut"
          },
          count: { $sum: 1 }
        }
      }]
    }
  }
  ])

  let res = await mongoUtil.db.collection('amendements').aggregate(query).toArray()

  if (res.length) {
    return {
      body: [
        ...res[0].t.map(val => ({ source: val._id.auteur, target: val._id.texteLegislatifRef, value: val.count })),
        ...res[0].u.map(val => ({ source: val._id.texteLegislatifRef, target: val._id.statut, value: val.count })),
      ]
    }
  } else {
    return {
      body: []
    }
  }
}
