from pymongo import MongoClient


mongo_url = "mongodb://127.0.0.1/dataViz"
db="dataViz"
collection="amendements-2"
client = MongoClient(mongo_url, retryWrites=False)[db][collection]

# nombre d'amendement par sort, etat et sous etat
# res = client.aggregate([
#     {
#         '$group': {
#             '_id': {
#                 'sort': '$sort',
#                 'etat': '$etat',
#                 'sousEtat': '$sousEtat'
#             },
#             'count': {
#                 '$sum': 1
#             }
#         }
#     }, {
#         '$project': {
#             '_id': 0,
#             'sort': '$_id.sort',
#             'etat': '$_id.etat',
#             'sousEtat': '$_id.sousEtat',
#             'count': 1
#         }
#     }
# ])

res = client.distinct("texteLegislatifRef")

print (list(res))