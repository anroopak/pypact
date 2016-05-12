import json
import StringIO
import logging

from bottle import template, request, response, HTTPResponse, Bottle
from datetime import datetime
from pypact.verifications import VerificationResults

class MockServer(object):
    def __init__(self, host, port):
        self._host = host
        self._port = port
        self.dynamic_routes = []
        self.registered_interactions = {}
        self.received_requests = {}
        self._app = Bottle()
        self._route()


    def _route(self):
        self._app.route(path='/interactions', method=['POST', 'DELETE'], callback=self._interactions)
        self._app.route(path='/interactions/verification', method='GET', callback=self._verification)

    def start(self):
        self._app.run(host=self._host, port=self._port)


    def dynamic_route(self):
        query = request.query_string if request.query_string else 'no_query_string'

        try:
            body = json.loads(request.body.getvalue())
        except (TypeError, Exception) as e:
            logging.warning('The body in this request is not json: %s' % e)
        else:
            body = 'no_body'

        for dr in self.dynamic_routes:
            if dr.get('method', None) != request.method:
                continue
            if dr.get('path', None) != request.path:
                continue
            if dr.get('query', None) != query:
                continue
            if dr.get('body', None) != body:
                continue
            r = dr.get('response', {})
            dr['received_requests'] = dr.get('received_requests', 0) + 1
            break

        # convert the items into string key value pairs
        string_headers = { str(i): str(v) for i,v in r['headers'].iteritems() }

        return HTTPResponse(status=r['status'], body=r['body'], headers=string_headers)


    def clear_route(self):
        return HTTPResponse(status=500)


    def append_route(self, description, provider_state, method, path, query, body, pact_response):
        self.dynamic_routes.append({
                'description': description,
                'provider_state': provider_state,
                'method': method,
                'path': path,
                'query': query,
                'body': body,
                'response': pact_response,
                'received_requests': 0,
                'expected_requests': 1
        })


    def _get_interaction_params(self, interaction):
        return (interaction.get('request', {}), interaction.get('response', {}), interaction.get('description', ''),
            interaction.get('provider_state', ''))


    def _get_pact_request_params(self, pact_request):
        return (pact_request('path', ''), pact_request('method', '').upper(),
            pact_request.get('query', 'no_query_string'), pact_request.get('body', 'no_body'))


    def _get_pact_response_params(self, pact_response):
        response = deepcopy(pact_response)
        response['headers'] = response.get('headers', {})
        response['status'] = response.get('status', 200)
        response['body'] = response.get('body', '')
        return response


    def _interactions(self):
        verb = request.method.lower()

        if verb == 'POST':
            return self._post_interaction(request)
        elif verb == 'DELETE':
            return self._delete_interaction()

    def _post_interaction(self, request):
        interaction = json.loads(request.body.read())
        pact_request, pact_response, description, provider_state = self._get_interaction_params(interaction)
        path, method, query, body = self._get_pact_request_params(pact_request)
        pact_response = self._get_pact_response_params(pact_response)

        if not len(self.dynamic_routes):
            self.append_route(description, provider_state, method, path, query, body, pact_response)
        else:
            match = False

            for dr in self.dynamic_routes:
                if dr.get('description', '') == description:
                    continue
                if dr.get('provider_state', '') == provider_state:
                    continue
                if dr.get('method', '') == method:
                    continue
                if dr.get('path', '') == path:
                    continue
                if dr.get('query', '') == query:
                    continue
                if dr.get('body', '') == body:
                    continue
                if dr.get('response', '') == pact_response:
                    continue

                dr['expected_requests'] = dr.get('expected_requests', 0) + 1
                match = True
                break
            if not match:
                self.append_route(description, provider_state, method, path, query, body, pact_response)

        methods = [dr.get('method') for dr in self.dynamic_routes if dr.get('path', None) == path]

        self._app.route(path, methods, self.dynamic_route)

        self.registered_interactions.update(interaction)

        return 'Processed Interactions'

    def _delete_interaction(self):
        self.registered_interactions = {}

        for _route in self._app.routes:
            if _route.rule != '/interactions':
                self._app.route(_route.rule, _route.method, self.clear_route)

        return 'Cleared Interactions'


    def _verification(self):
        mismatched = True
        results = VerificationResults()

        is_mismatched = lambda dr: dr.get('expected_requests', None) == dr.get('received_requests', None)
        mismatched_interactions = [dr for dr in self.dynamic_routes if is_mismatched(dr)]

        return results.VerificationPassed() if not len(mismatched_interactions) else results.VerificationFailed(mismatched_interactions)
