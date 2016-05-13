class Interaction(object):
    """
    Builder for interaction dictionaries
    """

    def __init__(self, add_method):
        self.add_method = add_method

        self.provider_state = None
        self.description = None
        self.request = None
        self.response = None

    def to_JSON(self):
        json = self.__dict__
        json.pop('add_method', None)
        return json

    def safe_assign(self, dictionary, key_values):
        dictionary.update({key: value for key, value in key_values.iteritems() if value})
        return dictionary

    def given(self, provider_state):
        self.provider_state = provider_state
        return self

    def upon_receiving(self, description):
        self.description = description
        return self

    def with_request(self, method, path, query=None, headers=None, body=None):
        data = {
            'method': method.lower(),
            'path': path,
            'query': query,
            'headers': headers,
            'body': body
        }

        self.request = self.safe_assign({}, data)

        return self

    def will_respond_with(self, status, headers=None, body=None):
        data = {
            'status': status,
            'headers': headers,
            'body': body
        }

        self.response = self.safe_assign({}, data)

        self.add_interaction()

        return self

    def add_interaction(self):
        self.add_method({
            'provider_state': self.provider_state,
            'description': self.description,
            'request': self.request,
            'response': self.response
        })
