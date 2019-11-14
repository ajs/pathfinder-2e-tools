
import json


# Location of the rules data file
PF2RulesFile = 'ogl-content/rules.json'


class PF2Rules:
    """
    A wrapper class that provides access to the rules datafile.
    """

    def __init__(self, infile, options):
        self.options = options
        self.data = json.loads(infile.read())
        self._hazards = None

    @property
    def threat_budget(self):
        return self.data['threat_budget']

    @property
    def encounter_costs(self):
        return self.data['encounter_costs']

    @property
    def creatures(self):
        return self.data['creatures']

    @property
    def hazards(self):
        if not self._hazards:
            self._hazards = [self._hazard_clean(h) for h in self.data['hazards']]
        return self._hazards

    @staticmethod
    def _hazard_clean(hazard):
        h = hazard.copy()
        h['Level'] = int(h.get('Level', 0))
        return h
