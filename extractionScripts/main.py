import json
from amandement import Amandement
from acteur import Acteur
from document import Document
from amendements14 import Amendement14
from pymongo import MongoClient
from os import walk, path


def walklevel(some_dir, level=1):
	some_dir = some_dir.rstrip(path.sep)
	assert path.isdir(some_dir)
	num_sep = some_dir.count(path.sep)
	for root, dirs, files in walk(some_dir):
		yield root, dirs, files
		num_sep_this = root.count(path.sep)
		if num_sep + level <= num_sep_this:
			del dirs[:]


def import_records(dir_name, db_name, obj_instance):
	mongo_url = "mongodb://127.0.0.1/dataViz"
	client = MongoClient(mongo_url, retryWrites=False)["dataViz"][db_name]

	# for root_m, dirs_m, files_m in walk(DIR_NAME):
	# 	print('!')
	# 	for dir_m in dirs_m:
	# print(dir_m)
	records = []
	for root, dirs, files in walk(dir_name):
		for file in files:
			with open(path.join(root, file)) as json_file:
				data = json.load(json_file)
				record = obj_instance(data)
				records.append(record)

	client.insert_many([record.__dict__ for record in records])


def import_amendements(schema):
	# DIR_NAME = 'C://Users//emixa//Downloads//Amendements_XV.json//json'
	DIR_NAME = 'C://Users//emixa//Downloads//Amendements_XV.json//json'

	mongo_url = "mongodb://127.0.0.1/dataViz"
	client = MongoClient(mongo_url, retryWrites=False)["dataViz"][schema]

	amandements = []
	for root, dirs, files in walk(DIR_NAME):
		# for root_m, dirs_m, files_m in walklevel(DIR_NAME, 1):
		# for dir_m in dirs_m:
		for file in files:
			with open(path.join(root, file)) as json_file:
				data = json.load(json_file)
				amandement = Amandement(data['amendement'])
				amandements.append(amandement)
				
		# if len(amandements) > 10000:
		# 	client.insert_many([amandement.__dict__ for amandement in amandements])
		# 	amandements = []

	client.insert_many([amandement.__dict__ for amandement in amandements])


		# for root, dirs, files in walk(path.join(root_m, dir_m)):
	# 	for file in files_m:
	# 		# //PIONANR5L15B0422//AMANR5L15PO59051B0422P0D1N000002.json
	# 		with open(path.join(root, file)) as json_file:
	# 			data = json.load(json_file)
	# 			# try:
	# 			amandement = Amandement(data['amendement'])
	# 			# except e:
	# 			# 	print(path.join(root_m, dir_m))
	# 			# 	print(data)
	#
	# 			amandements.append(amandement)
	#
	# client.insert_many([amandement.__dict__ for amandement in amandements])


def update_acteur():

	mongo_url = "mongodb://127.0.0.1/dataViz"
	client = MongoClient(mongo_url, retryWrites=False)["dataViz"]["acteurs"]

	from operator import attrgetter

	db_deputees = list(client.find().sort("nom", 1).sort("prenom", 1).limit(5000))
	# db_deputees = sorted(db_deputees, key=attrgetter('prenom', 'nom'))
	# for d in db_deputees:
	# 	print(d['prenom'] + ' ' + d['nom'])

	# print(db_deputees)
	# print(str([d['prenom'] + ' ' + d['nom'] for d in db_deputees]))
	print()

	count = 0

	with open('deputees.json', encoding='utf-8') as json_file:
		deputees = json.load(json_file)
		for deputee in deputees:
			for db_deputee in db_deputees:
				# print(db_deputee['prenom'] + ' ' + db_deputee['nom'])
				if deputee['nom'] == db_deputee['prenom'] + ' ' + db_deputee['nom']:
					count = count + 1
					db_deputees.remove(db_deputee)
					try:
						client.update_one({"_id": db_deputee['_id']}, {
							"$set": {
								"place": deputee['place'],
								"departement": deputee['departement'],
								"circo": deputee['circo'],
								"groupe": deputee['groupe']
							}
						})
					except:
						print(deputee)
					break
			# print(deputee['nom'], deputee['nom'] in [d['prenom'] + ' ' + d['nom'] for d in db_deputees])
	print(count)
	print(db_deputees)


def import_missing_deputees():
	import csv
	deputees = []
	with open('missing_deputees.csv', newline='') as csvfile:
		csv_reader = csv.reader(csvfile, delimiter=',')
		headers = next(csv_reader, None)
		for row in csv_reader:
			deputee = {}
			for header, val in zip(headers, row):
				deputee[header] = val
			deputees.append(deputee)

	group_conversion = {
		'LR'    : 'Les Républicains',
		'X'     : 'La France insoumise',
		'LREM'  : 'La République en Marche',
		'GDR'   : 'Gauche démocrate et républicaine',
		'NI'    : 'Non inscrit',
		'Modem' : 'Mouvement Démocrate (MoDem) et Démocrates apparentés',
		'PS'    : 'Socialistes et apparentés',
		'Y'     : 'Libertés et Territoires',
		'AE'    : 'Agir ensemble',
		'UDI'   : 'UDI et Indépendants'
	}

	for deputee in deputees:
		try:
			deputee['groupe'] = group_conversion[deputee['groupe']]
		except Exception as e:
			print(e)
			print(deputee)

	mongo_url = "mongodb://127.0.0.1/dataViz"
	client = MongoClient(mongo_url, retryWrites=False)["dataViz"]["acteurs"]
	client.insert_many(deputees)


def import_amendements_14():
	mongo_url = "mongodb://127.0.0.1/dataViz"
	client = MongoClient(mongo_url, retryWrites=False)["dataViz"]["amendements14"]

	index = 0
	with open('C://Users//emixa//Downloads//amendements XIV//Amendements//Amendements_XIV.json') as json_file:
		obj = json.load(json_file)
		for texte in obj['textesEtAmendements']['texteleg']:
			# with open('amend14//dump' + str(index) + '.json', 'w') as outfile:
			# 	json.dump(texte, outfile)
			print(index)
			index = index + 1
			records = []
			amendements = texte['amendements']['amendement']
			if isinstance(amendements, list):
				for amend in texte['amendements']['amendement']:
					records.append(Amendement14(amend))
			else:
				records.append(Amendement14(amend))

			client.insert_many([record.__dict__ for record in records])


if __name__ == '__main__':
	# import_amendements('amendements')
	# import_records('C://Users//emixa//Downloads//Dossiers_Legislatifs_XV.json//json//document', 'documents', Document)
	#
	# import_records('C://Users//emixa//Downloads//AMO10_deputes_actifs_mandats_actifs_organes_XV.json//json//acteur', 'acteurs', Acteur)
	# import_missing_deputees()
	update_acteur()
	# import_records('C://Users//emixa//Downloads//AMO30_tous_acteurs_tous_mandats_tous_organes_historique.json//json//acteur', 'acteurs-all', Acteur)
	# import_amendements_14()

