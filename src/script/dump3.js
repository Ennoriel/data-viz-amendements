/**
 * Outputs a mongodb request
 */
require('dotenv').config()
const mongoUtil = require('../mongo.util');

mongoUtil.init().then(async () => {
  let auteurFromAmendements = await (await mongoUtil.db.collection('amendements-3').aggregate([
    {
      $match: {
        texteLegislatifRef: "PRJLANR5L15B3875"
      }
    }, {
      $group: {
        _id: {
          sort: "$sort",
          etat: "$etat",
          sousEtat: "$sousEtat"
        },
        count: {
          $sum: 1
        }
      }
    },
    {
      $sort: {
        "_id.etat": 1
      }
    }
  ])).toArray()

  console.log(JSON.stringify(auteurFromAmendements, null, 2))

  mongoUtil.client.close()
})