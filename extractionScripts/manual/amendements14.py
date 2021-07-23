from record import Record
import json


class Amendement14(Record):

	def __init__(self, jsonObj):

		# uid
		# texteLegislatifRef
		# auteur
		# isDepute
		# depot
		# sort
		super(Amendement14, self).get_json_val('uid', jsonObj, ['uid'], False)
		super(Amendement14, self).get_json_val('texteLegislatifRef', jsonObj, ['identifiant', 'saisine', 'refTexteLegislatif'], False)
		super(Amendement14, self).get_json_val('auteur', jsonObj, ['signataires', 'auteur', 'acteurRef'], False)
		if not hasattr(self, 'auteur'):
			super(Amendement14, self).get_json_val('auteur', jsonObj, ['signataires', 'auteur', 'acteur'], False)
		super(Amendement14, self).get_json_val('groupePolitiqueRef', jsonObj, ['signataires', 'auteur', 'groupePolitiqueRef'], False)
		super(Amendement14, self).get_json_val('isDepute', jsonObj, ['signataires', 'auteur', 'typeAuteur'], False)
		if hasattr(self, 'isDepute'):
			if self.isDepute == "Gouvernement":
				self.auteur = "Gouvernement"
				self.groupePolitiqueRef = "Gouvernement"
			else:
				self.isDepute = True if self.isDepute == "Depute" else False
		if not hasattr(self, 'groupePolitiqueRef'):
			self.groupePolitiqueRef = 'Inconnu'

		super(Amendement14, self).get_json_val('depot', jsonObj, ['dateDepot'], True)
		if hasattr(self, 'depot'):
			self.depot = {
				"date": self.depot,
				"year": self.depot.year,
				"month": self.depot.month,
				"week": self.depot.isocalendar()[1],
				"day": int(self.depot.strftime("%d"))
			}

		super(Amendement14, self).get_json_val('sort', jsonObj, ['sort', 'sortEnSeance'], False)
		if not hasattr(self, 'sort'):
			super(Amendement14, self).get_json_val('sort', jsonObj, ['etat'], False)

		if len(self.__dict__.keys()) < 7:
			print('==')
			print([a for a in ['uid', 'texteLegislatifRef', 'auteur', 'isDepute', 'groupePolitiqueRef', 'depot', 'sort'] if a not in self.__dict__.keys()])
			print(self.__dict__)
			print(json.dumps(jsonObj, indent=4, sort_keys=True))
			# raise Exception('ee')


		pass
