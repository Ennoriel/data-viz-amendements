from datetime import datetime


class Record:

	def get_json_val(self, obj_key, json, keys, is_date, id_date_long=False):
		val = json
		try:
			for key in keys:
				val = val[key]
			if isinstance(val, str):
				setattr(self, obj_key, datetime.strptime(val, '%Y-%m-%d') if is_date else datetime.strptime(val[0:10], '%Y-%m-%d') if id_date_long else val)
		except Exception as e:
			pass
			# print('did not find ' + '.'.join(keys) + ' in:')
			# print(json)
			# print(e)
		finally:
			return self
