from record import Record


class Document(Record):

	def __init__(self, json):

		json = json['document']

		# "uid": "ACINANR5L15B0012"
		super(Document, self).get_json_val('uid', json, ['uid'], False)

		# "denominationStructurelle": "Projet de loi"
		super(Document, self).get_json_val('denominationStructurelle', json, ['denominationStructurelle'], False)

		# "titres", "titrePrincipal": "Accord international sur le projet..."
		super(Document, self).get_json_val('titre', json, ['titres', 'titrePrincipal'], False)

		# "titres", "titrePrincipalCourt": "convention d\u2019entraide judiciaire..."
		super(Document, self).get_json_val('titreCourt', json, ['titres', 'titrePrincipalCourt'], False)

		# "cycleDeVie", "chrono", "dateDepot":	"2019-06-14T00:00:00.000+02:00"
		super(Document, self).get_json_val('dateDepot', json, ['cycleDeVie', 'chrono', 'dateDepot'], False, True)

		pass
