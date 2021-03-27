const express = require("express");
const Amendements = require('./amendements');
const Documents = require('./documents');
const Acteurs = require('./acteurs');

var router = express.Router();

router.post('/', async function(req, res, next) {
    res.send({ data: await Amendements.get(req.body._id) });
});

router.post('/agg', async function(req, res, next) {
    res.send(await Amendements.agg());
});

router.post('/projectAuteurSort', async function(req, res, next) {
    res.send(await Amendements.projectAuteurSort(req.body.documentId));
});

router.post('/projectGroupNewSort', async function(req, res, next) {
    res.send(await Amendements.projectGroupNewSort(req.body.documentId));
});

router.post('/projectDayMonth', async function(req, res, next) {
    res.send(await Amendements.projectDayMonth(req.body.documentId, req.body.acteurId));
});

router.post('/projectNewSortDate', async function(req, res, next) {
    res.send(await Amendements.projectNewSortDate(req.body.sort));
});

router.post('/sankyActeurDocumentSort', async function(req, res, next) {
    res.send(await Amendements.sankyActeurDocumentSort(req.body.documentIds, req.body.acteurIds));
});

router.post('/documents', async function(req, res, next) {
    res.send(await Documents.get());
});

router.post('/acteurs', async function(req, res, next) {
    res.send(await Acteurs.get());
});

module.exports = router