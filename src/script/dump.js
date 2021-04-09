/**
 * Initializes the amend-group-newSort collection used for the group / new sort histogram chart
 */
require('dotenv').config()
const mongoUtil = require('../mongo.util');

mongoUtil.init().then(async() => {
    let auteurFromAmendements = await (await mongoUtil.db.collection('amendements').distinct("auteur")).sort()
    let auteurFromActeurs = await (await mongoUtil.db.collection('acteurs').distinct("uid")).sort()

    let diff = auteurFromAmendements.filter(t => !auteurFromActeurs.includes(t))
    console.log(JSON.stringify(diff.length))

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
            '$group': {
                '_id': {
                    'statut': '$statut',
                    'auteur': '$auteur',
                    'texteLegislatifRef': '$texteLegislatifRef'
                },
                'count': {
                    '$sum': 1
                }
            }
        // }, {
        //     '$addFields': {
        //         'newSort': {
        //             '$cond': [{
        //                 '$not': {
        //                 '$in': [
        //                         '$_id.sort', [
        //                         // "Tombé",
        //                         // "Retiré",
        //                         // "Rejeté",
        //                         // "Non soutenu",
        //                         "Irrecevable 40",
        //                         "Irrecevable",
        //                             // "En traitement",
        //                             // "En recevabilité",
        //                             // "Adopté",
        //                             // "A discuter"
        //                         ]
        //                     ]
        //                 }
        //             }, 'Autre sort', '$_id.sort']
        //         }
        //     }
        // }, {
        //     '$group': {
        //         '_id': {
        //             'sort': '$newSort',
        //             'auteur': '$_id.auteur',
        //             'texteLegislatifRef': '$_id.texteLegislatifRef'
        //         },
        //         'count': {
        //             '$sum': '$count'
        //         }
        //     }
        }, {
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
            '$group': {
                '_id': {
                    'statut': '$_id.statut',
                    'groupe': '$groupe',
                    'texteLegislatifRef': '$_id.texteLegislatifRef'
                },
                'count': {
                    '$sum': '$count'
                }
            }
        }, {
            '$lookup': {
                'from': 'documents',
                'localField': '_id.texteLegislatifRef',
                'foreignField': 'uid',
                'as': 'document'
            }
        }, {
            '$unwind': {
                'path': '$document'
            }
        }, {
            '$project': {
                '_id': 0,
                'groupe': '$_id.groupe',
                'document': '$document.titre',
                'texteLegislatifRef': '$document.uid',
                'statut': '$_id.statut',
                'count': 1
            }
        },
        {
            '$merge': 'amend-group-statut'
        }
    ]).toArray()
    console.log(new Date().toISOString())

    console.log(res)
    mongoUtil.client.close()
})