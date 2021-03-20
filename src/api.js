const express = require("express");
const Amendements = require('./amendements');

var router = express.Router();

router.post('/', async function (req, res, next) {
  console.log(req.body)
  res.send({data: await Amendements.get(req.body._id)});
});

router.post('/agg', async function (req, res, next) {
  console.log(req.body)
  res.send(await Amendements.agg());
});

module.exports = router
