import MongoClient from 'mongodb';

class MongoUtil {
  async init() {
    if (!this.db) {
      this.client = await new MongoClient(process.env['MONGO_URI'], { useUnifiedTopology: true, authSource: process.env['MONGO_DB'] });
      await this.client.connect();
      this.db = this.client.db(process.env['MONGO_DB']);
    }
  }
}

export default new MongoUtil();