var MongoUtil = require('./mongo.util');

class Acteurs {
  
  async get() {
    return await MongoUtil.db.collection('acteurs')
                              .find({})
                              .sort({prenom: 1, nom: 1})
                              .toArray();
  }
}

module.exports = new Acteurs();