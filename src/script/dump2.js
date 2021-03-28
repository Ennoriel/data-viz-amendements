/**
 * Initializes the amend-sort-group-date collection used for the sort / date / groupe linear charts
 */
require('dotenv').config()
const mongoUtil = require('../mongo.util');

mongoUtil.init().then(async() => {
    let auteurFromAmendements = await (await mongoUtil.db.collection('amendements').distinct("auteur")).sort()
    let auteurFromActeurs = await (await mongoUtil.db.collection('acteurs').distinct("uid")).sort()

    let diff = auteurFromAmendements.filter(t => !auteurFromActeurs.includes(t))
    console.log(JSON.stringify(diff.length))
    console.log(diff)

    let auteurPlusDepute = await (await mongoUtil.db.collection('acteurs-all').find({ uid: { $in: diff } })).toArray()
        // console.log(auteurPlusDepute.map(a => `${a.uid},${a.nom},${a.prenom}`))
    console.log(auteurPlusDepute.map(apd => apd.uid))

    diff = auteurFromActeurs.filter(t => !auteurFromAmendements.includes(t))
    console.log(JSON.stringify(diff.length))



    console.log(new Date().toISOString())
    let res = await mongoUtil.db.collection('amendements').aggregate([{
            // suppression de données sans date
            '$match': {
                'depot.year': {
                    '$exists': 1
                },
                'depot.month': {
                    '$exists': 1
                },
                'isDepute': true
            }
        }, {
            // groupe par sort, auteur, date
            '$group': {
                '_id': {
                    'sort': '$sort',
                    'auteur': '$auteur',
                    'year': '$depot.year',
                    'month': '$depot.month'
                },
                'count': {
                    '$sum': 1
                }
            }
        }, {
            // Jointure acteurs pour récupérer le groupe politique
            '$lookup': {
                'from': 'acteurs',
                'localField': '_id.auteur',
                'foreignField': 'uid',
                'as': 'acteur'
            }
        }, {
            '$unwind': {
                'path': '$acteur',
                'preserveNullAndEmptyArrays': true
            }
        }, {
            '$addFields': {
                'groupe': {
                    '$ifNull': [
                        '$acteur.groupe', 'Inconnu (arrêt de mandat)'
                    ]
                }
            }
        }, {
            // Groupe sur le sort, groupe et date
            '$group': {
                '_id': {
                    'sort': '$_id.sort',
                    'groupe': '$groupe',
                    'year': '$_id.year',
                    'month': '$_id.month'
                },
                'count': {
                    '$sum': '$count'
                }
            }
        }, {
            // Groupe sur le groupe date pour calculer le nombre total d'amendements
            '$group': {
                '_id': {
                    'groupe': '$_id.groupe',
                    'year': '$_id.year',
                    'month': '$_id.month'
                },
                'data': {
                    '$push': {
                        'sort': '$_id.sort',
                        'count': '$count'
                    }
                },
                'total': {
                    '$sum': '$count'
                }
            }
        }, {
            '$unwind': {
                'path': '$data'
            }
        }, {
            // Calcul du nombre d'amendement par groupe politique, mois et sort
            '$addFields': {
                'p': {
                    '$round': [{
                        // '$multiply': [{
                        '$divide': [
                                '$data.count', '$total'
                            ]
                            // }, 100]
                    }, 3]
                },
                'date': {
                    '$dateFromParts': {
                        'year': '$_id.year',
                        'month': '$_id.month'
                    }
                }
            }
        }, {
            '$sort': {
                'date': 1,
                '_id.groupe': 1
            }
        }, {
            // Groupe par groupe et sort
            '$group': {
                '_id': {
                    'groupe': '$_id.groupe',
                    'sort': '$data.sort'
                },
                'records': {
                    '$push': {
                        'date': '$date',
                        'count': '$data.count',
                        'pourcentage': '$p'
                    }
                }
            }
        }, {
            // Groupe par sort afin d'avoir une structure à deux niveaux
            '$group': {
                '_id': '$_id.sort',
                'groupRecords': {
                    '$push': {
                        'records': '$records',
                        'groupe': '$_id.groupe'
                    }
                }
            }
        },
        {
            '$merge': 'amend-sort-group-date'
        }
    ]).toArray()
    console.log(new Date().toISOString())

    console.log(res)
    mongoUtil.client.close()
})