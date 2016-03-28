import json
import pypact
import os

metadata = {"pactSpecificationVersion": "1.1.0"}

class Builder(object):
	
	def __init__(self, consumer, provider, port, path):
		self.port = port
		self.path = path
		self.consumer = self.create_consumer(consumer)
		self.provider = self.create_provider(provider)
		self.service = self.create_pact()
		self.create_pact_folder()


	def create_consumer(self, consumer):
		return pypact.Consumer(consumer)


	def create_provider(self, provider):
		return pypact.Provider(provider)


	def create_pact(self):
		return self.consumer.has_pact_with(self.provider, self.port)

	def create_pact_folder(self):
		if os.path.exists(self.path):
			return
		os.makedirs(self.path)


	def parse_participants(self):
		if self.consumer.name == "":
			raise pypact.PyPactNullConsumerException(
                "Consumer must not be null")
		if self.provider.name == "":
			raise pypact.PyPactNullProviderException(
                "Provider must not be null")
		return {"consumer": self.consumer.name.lower(), "provider": self.provider.name.lower()}


	def persist_pact(self, pact, interactions):
		file_name = self.consumer.name.lower().replace(" ","_") + "-" + self.provider.name.lower().replace(" ","_") + ".json"
		pact['interactions'] = interactions
		pact['metadata'] = metadata

		self.path = self.path + "/" + file_name

		with open(self.path, 'w') as outfile:
			json.dump(pact, outfile, sort_keys=True, indent=4, separators=(',',':'))