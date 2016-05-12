from pypact.exceptions import PyPactServiceException
from pypact.interaction import Interaction


class MockService(object):
    """
    Interface to interact with pact mock server.
    """

    def __init__(self, consumer, provider, port):
        self.consumer = consumer
        self.provider = provider
        self.port = port

        self.stopped = True
        self.interactions = []


    def given(self, state):
        return self.interaction_builder(self.add_interaction).given(state)


    def upon_receiving(self, description):
        return (
            self.interaction_builder(self.add_interaction)
                .upon_receiving(description))


    def interaction_builder(self, add_method):
        return Interaction(add_method)


    def add_interaction(self, interaction):
        """
        Add a new interaction to the mock service.
        """
        self.interactions.append(interaction)


    def start(self):
        """
        Start the mock service, loading the interactions into the pact server.
        """
        if not self.stopped:
            raise PyPactServiceException("Cannot start already started MockService.")

        self.stopped = False


    def end(self):
        """
        End the mock service, verifing the interactions with the pact server.
        """
        if self.stopped:
            raise PyPactServiceException(
                "Cannot end already ended MockService.")

        self.stopped = True


    def __enter__(self):
        self.start()


    def __exit__(self, type, value, traceback):
        self.end()
