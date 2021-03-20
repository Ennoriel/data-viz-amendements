const { MongoClient } = require('mongodb');

class MongoUtil {
  constructor() {
    this.client = new MongoClient(process.env.MONGO_URI, { useUnifiedTopology: true });
  }
  async init() {
    await this.client.connect();
    this.db = this.client.db(process.env.MONGO_DB);
  }
}

module.exports = new MongoUtil();