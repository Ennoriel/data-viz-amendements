from record import Record


class Acteur(Record):

	def __init__(self, json):

		json = json['acteur']

		# acteur.uid.#text				PA508
		super(Acteur, self).get_json_val('uid', json, ['uid', '#text'], False)

		# etatCivil.ident.civ			Mme
		super(Acteur, self).get_json_val('civ', json, ['etatCivil', 'ident', 'civ'], False)

		# etatCivil.ident.prenom		Gis\u00e8le
		super(Acteur, self).get_json_val('prenom', json, ['etatCivil', 'ident', 'prenom'], False)

		# etatCivil.ident.nom				Bi\u00e9mouret
		super(Acteur, self).get_json_val('nom', json, ['etatCivil', 'ident', 'nom'], False)

		# etatCivil.ident.trigramme		GB
		super(Acteur, self).get_json_val('trigramme', json, ['etatCivil', 'ident', 'trigramme'], False)

		# etatCivil.infoNaissance.dateNais		1952-06-16
		super(Acteur, self).get_json_val('dateNaissance', json, ['etatCivil', 'infoNaissance', 'dateNais'], True)

		# profession.libelleCourant		Assistante parlementaire
		super(Acteur, self).get_json_val('profession', json, ['profession', 'libelleCourant'], False)

		pass
