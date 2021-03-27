var MongoUtil = require('./mongo.util');
ObjectID = require('mongodb').ObjectID

class Amendements {

    async get(_id) {
        return MongoUtil.db.collection('amendements').find({ _id: ObjectID(_id) }).toArray();
    }

    async agg() {
        return MongoUtil.db.collection('amendements').aggregate(
            [{
                '$facet': {
                    'dp': [{
                        '$sortByCount': '$auteur'
                    }]
                }
            }, {
                '$unwind': {
                    'path': '$dp'
                }
            }, {
                '$replaceRoot': {
                    'newRoot': '$dp'
                }
            }, ]
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

        query.push(...[{
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
                    as: 'acteur'
                }
            },
            {
                $unwind: {
                    path: '$acteur'
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

        // let res = await MongoUtil.db.collection('amendements').aggregate(query).toArray();
        // return res.map(({auteur, test, statuts}) => ({auteur: test && `${test.prenom} ${test.nom}` || auteur, ...statuts}))


        return MongoUtil.db.collection('amendements')
            .aggregate(query)
            .toArray()
            .then(res => res
                .map(({ auteur, acteur, statuts }) => ({ auteur: acteur && `${acteur.prenom} ${acteur.nom}` || auteur, ...statuts }))
            )
    }

    projectDayMonth(documentId, acteurId) {

        let query = []
        let match = {}

        if (documentId) match.texteLegislatifRef = documentId
        if (acteurId) match.auteur = acteurId

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

        return MongoUtil.db.collection('amendements').aggregate(query).toArray();
    }

    async projectGroupNewSort(documentId) {
        let query = []
        let match = {}

        if (documentId) match.texteLegislatifRef = documentId

        query.push(
            ...[{
                    '$match': match
                },
                {
                    '$group': {
                        '_id': {
                            'sort': '$sort',
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
                                'k': '$_id.sort',
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
        )

        return MongoUtil.db.collection('amend-group-newSort')
            .aggregate(query)
            .toArray()
            .then(res => res
                .map(({ groupe, res, count }) => ({ groupe, ...res }))
            )
    }

    async projectNewSortDate(sort) {

        return MongoUtil.db.collection('amend-sort-group-date')
            .findOne({ _id: sort })
    }

    async sankyActeurDocumentSort(documentIds, acteurIds) {
        let query = []
        let match = {}

        if (documentIds) match.texteLegislatifRef = { $in: documentIds }
        if (acteurIds) match.auteur = { $in: acteurIds }

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
                                sort: "$sort"
                            },
                            count: { $sum: 1 }
                        }
                    }]
                }
            }
        ])

        let res = await MongoUtil.db.collection('amendements').aggregate(query).toArray()

        if (res.length) {
            return [
                ...res[0].t.map(val => ({ source: val._id.auteur, target: val._id.texteLegislatifRef, value: val.count })),
                ...res[0].u.map(val => ({ source: val._id.texteLegislatifRef, target: val._id.sort, value: val.count })),
            ]
        } else {
            return []
        }
    }
}
module.exports = new Amendements();