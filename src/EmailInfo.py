'''
	Date: 2019/08/10
	Author: Eleven
	Description: Email info (Object)
'''
import json

class EmailInfo(object):
	def __init__(self, dict):
		self.__dict__.update(dict)

	def toJson(self):
		return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True)