class ExampleType(object):
	def __init__(self, classifications, features):
		self.classifications = classifications
		self.features = features
		self.feature_lookup = {}
		for index, feature in enumerate(self.features):
			self.feature_lookup[feature] = index

	def get_index(self, feature):
		return self.feature_lookup[feature]

	def create_example(self, id, input_vector, output):
		return Example(self, id, input_vector, output)

	def __repr__(self):
		return str(self)

	def __str__(self):
		return str([feature.name for feature in self.features])

class Example(object):
	def __init__(self, type, id, input_vector, output):
		self.type = type
		self.id = id
		self.input_vector = input_vector
		self.output = output

	def get_value(self, feature):
		feature_index = self.type.get_index(feature)
		if 0 <= feature_index < len(self.input_vector):
			return self.input_vector[feature_index]
		return None

	def __repr__(self):
		return str(self)

	def __str__(self):
		rep = "Type: " + str(self.type) + "\n"
		rep += "ID: " + self.id + "\n"
		rep += "Input vector: " + str(self.input_vector) + "\n"
		rep += "Output: " + self.output
		return rep
