from json import dumps as to_json
from requests import Session


CLIENT_HEADERS = {
    'X-Pact-Mock-Service': 'true',
    'Content-Type': 'application/json'
}


class MockServerClient(Session):

    def __init__(self, base_uri, *args, **kwargs):
        super(MockServerClient, self).__init__(*args, **kwargs)

        self.base_uri = base_uri
        self.headers.update(CLIENT_HEADERS)

    def full_uri(self, endpoint):
        _endpoint = endpoint[1:] if endpoint.startswith('/') else endpoint
        return '{}/{}'.format(self.base_uri, _endpoint)

    def get_verification(self):
        return self.get(self.full_uri('interactions/verification')).text

    def put_interactions(self, interaction):
        self.put(self.full_uri('interactions'), data=to_json(interaction))

    def delete_interactions(self):
        return self.delete(self.full_uri('interactions')).text

    def post_interactions(self, interaction):
        return self.post(self.full_uri('interactions'), data=to_json(interaction)).text

    def post_pact(self, pact_details):
        self.post(self.full_uri('pact'), data=to_json(pact_details))
