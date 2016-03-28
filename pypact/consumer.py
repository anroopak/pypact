"""Provides API for managing service consumers"""
from pypact.service import MockService
from pypact.interaction import Interaction

class Consumer(object):

    def __init__(self, name, service_cls=MockService, interaction=Interaction):
        self.name = name
        self.service_cls = MockService
        self.interaction = Interaction

    def has_pact_with(self, provider, port):
        return self.service_cls(
            consumer=self,
            provider=provider,
            port=port)
