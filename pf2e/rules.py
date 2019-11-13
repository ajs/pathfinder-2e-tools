
import json


PF2RulesFile = 'ogl-content/rules.json'


class PF2Rules:
	def __init__(self, infile, options):
		self.options = options
		self.data = json.loads(infile.read())

	@property
	def threat_budget(self):
		return self.data['threat_budget']

	@property
	def encounter_costs(self):
		return self.data['encounter_costs']

	@property
	def creatures(self):
		return self.data['creatures']
