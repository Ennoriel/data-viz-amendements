require('dotenv').config()
const express = require("express");
const sirv = require('sirv');
const compress = require('compression')();
const cors = require('cors');
const mongoUtil = require('./mongo.util');
const api = require('./api');

const app = express();

app.use(cors())

app.use((req, res, next) => {
    console.log(`${req.method} ${req.url}`)
    next();
})

app.use(express.json());
app.use(express.urlencoded());

const assets = sirv(`${__dirname}/../public`, {
    maxAge: 1,
    immutable: true
});
app.use(compress, assets)

app.use('/api', api)

mongoUtil.init().then(() => {
    console.log('DB started')
    return app.listen(process.env.PORT || 3000)
}).then(() => {
    console.log('server started')
})