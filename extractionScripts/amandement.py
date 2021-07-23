from datetime import datetime
from html import unescape
from json import dumps


class Amandement:

	def __init__(self, json):


		self.uid = json['uid']
		# self.timestamp = datetime.fromtimestamp(int(json['chronotag'])/1000.0)
		# self.identification = json['identification']
		# self.examenRef = json['examenRef']
		self.texteLegislatifRef = json['texteLegislatifRef']
		if 'signataires' in json:
			if 'auteur' in json['signataires']:
				if 'acteurRef' in json['signataires']['auteur']:
					if isinstance(json['signataires']['auteur']['acteurRef'], str):
						self.auteur = json['signataires']['auteur']['acteurRef']
						self.isDepute = True
					else:
						if 'gouvernementRef' in json['signataires']['auteur']:
							self.isDepute = False
							self.auteur = json['signataires']['auteur']['gouvernementRef']
						else:
							print(dumps(json, indent=2, sort_keys=True))
							raise ValueError('wrong sort type')
				else:
					raise Exception('e')
				# if 'typeAuteur' in json['signataires']['auteur']:
				# 	self.typeAuteur = json['signataires']['auteur']['typeAuteur']
				# else:
				# 	raise Exception('e')
			else:
				raise Exception('e')
			# if 'cosignataires' in json['signataires']:
			# 	if'acteurRef' in json['signataires']['cosignataires']:
			# 		self.coAuteurs = json['signataires']['cosignataires']['acteurRef']
		else:
			raise Exception('e')

		if isinstance(json['cycleDeVie']['dateDepot'], str):
			date = datetime.strptime(json['cycleDeVie']['dateDepot'], '%Y-%m-%d')
			self.depot = {
				"date": date,
				"year": date.year,
				"month": date.month,
				"week": date.isocalendar()[1],
				"day": int(date.strftime("%d"))
			}
		# elif isinstance(json['cycleDeVie']['datePublication'], str):
		# 	self.datePublication = datetime.strptime(json['cycleDeVie']['datePublication'], '%Y-%m-%d')
		# if isinstance(json['cycleDeVie']['dateSort'], str):
		# 	self.dateSort = datetime.strptime(json['cycleDeVie']['dateSort'][0:10], '%Y-%m-%d')
		# if isinstance(json['cycleDeVie']['sort'], str):
		# 	self.sort = json['cycleDeVie']['sort']
		# else:

		try:
			if isinstance(json['cycleDeVie']['sort'], str):
				self.sort = json['cycleDeVie']['sort']
			else:
				self.sort = 'Aucun'
		except:
			self.sort = 'Aucun'
			pass

		try:
			self.sousEtat = json['cycleDeVie']['etatDesTraitements']['sousEtat']['libelle']
		except:
			self.sousEtat = 'Aucun'
			pass

		try:
			self.etat = json['cycleDeVie']['etatDesTraitements']['etat']['libelle']
		except:
			self.etat = 'Aucun'
			print(dumps(json, indent=2, sort_keys=True))

		if self.sort == 'Aucun':
			if self.etat in ['En traitement', 'En recevabilité', 'A discuter'] :
				self.statut = 'En traitement'
			elif self.etat == 'Retiré':
				self.statut = 'Non adopté'
			else:
				self.statut = self.etat
		elif self.sort == 'Adopté':
			self.statut = 'Adopté'
		else:
			self.statut = 'Non adopté'


		# if 'dispositif' in json['corps']['contenuAuteur']:
		# 	self.dispositif = unescape(json['corps']['contenuAuteur']['dispositif'])
		# if 'exposeSommaire' in json['corps']['contenuAuteur']:
		# 	self.exposeSommaire = unescape(json['corps']['contenuAuteur']['exposeSommaire'])

		# if len(self.__dict__.keys()) < 6:
		# 	print('==')
		# 	print([a for a in ['uid', 'texteLegislatifRef', 'auteur', 'isDepute', 'groupePolitiqueRef', 'depot', 'sort'] if a not in self.__dict__.keys()])
		# 	print(self.__dict__)
		# 	print(dumps(json, indent=4, sort_keys=True))
		# 	# raise Exception('ee')
