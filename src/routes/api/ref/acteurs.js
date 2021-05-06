import mongoUtil from '$lib/db'

export async function post() {
  return {
    body: await mongoUtil.db.collection('acteurs')
      .find({})
      .sort({ prenom: 1, nom: 1 })
      .toArray()
  }
}