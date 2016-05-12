from json import dump as to_json
from os import makedirs
from os.path import exists, join as join_path

from pypact.consumer import Consumer
from pypact.provider import Provider
from pypact.exceptions import PyPactNullProviderException, PyPactNullConsumerException

metadata = {'pactSpecificationVersion': '1.1.0'}


class Builder(object):

    def __init__(self, consumer, provider, port, path):
        self.port = port
        self.path = path
        self.consumer = self.create_consumer(consumer)
        self.provider = self.create_provider(provider)
        self.service = self.create_pact()
        self.create_pact_folder()

    def create_consumer(self, consumer):
        return Consumer(consumer)

    def create_provider(self, provider):
        return Provider(provider)

    def create_pact(self):
        return self.consumer.has_pact_with(self.provider, self.port)

    def create_pact_folder(self):
        if not exists(self.path):
            makedirs(self.path)

    def parse_participants(self):
        if not self.consumer.name:
            raise PyPactNullConsumerException('Consumer must not be null')
        if not self.provider.name:
            raise PyPactNullProviderException('Provider must not be null')
        return {'consumer': self.consumer.name.lower(), 'provider': self.provider.name.lower()}

    def persist_pact(self, pact, interactions):
        file_name = '{}-{}.json'.format(self.consumer.name, self.provider.name).lower().replace(' ', '_')
        pact['interactions'] = interactions
        pact['metadata'] = metadata

        self.path = join_path(self.path, file_name)

        with open(self.path, 'w') as outfile:
            to_json(pact, outfile, sort_keys=True, indent=4, separators=(',', ':'))
