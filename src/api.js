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

router.post('/projectAuteurStatut', async function (req, res, next) {
    res.send(await Amendements.projectAuteurStatut(req.body.documentId));
});

router.post('/projectGroupStatut', async function (req, res, next) {
    res.send(await Amendements.projectGroupStatut(req.body.documentId));
});

router.post('/projectDayMonth', async function(req, res, next) {
    res.send(await Amendements.projectDayMonth(req.body.documentId, req.body.acteurId));
});

router.post('/projectStatutDate', async function (req, res, next) {
    res.send(await Amendements.projectStatutDate(req.body.statut));
});

router.post('/sankyActeurDocumentStatut', async function (req, res, next) {
    res.send(await Amendements.sankyActeurDocumentStatut(req.body.documentIds, req.body.acteurIds));
});

router.post('/documents', async function(req, res, next) {
    res.send(await Documents.get());
});

router.post('/acteurs', async function(req, res, next) {
    res.send(await Acteurs.get());
});

module.exports = router