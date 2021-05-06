import mongoUtil from '$lib/db'

export async function post({ body }) {
  return {
    body: await mongoUtil.db.collection('amend-statut-group-date')
      .findOne({ _id: body.statut })
  }
}
