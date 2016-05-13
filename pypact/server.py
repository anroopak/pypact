from copy import deepcopy
from json import loads as from_json
from logging import warning as warn
from bottle import request, HTTPResponse, Bottle

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

        body = request.body.getvalue()

        if body:
            try:
                body = from_json(body)
            except (TypeError, Exception) as e:
                warn('The body in this request is not json: %s' % (e))
        else:
            body = 'no_body'

        for dr in self.dynamic_routes:
            if dr['method'] != request.method:
                continue
            if dr['path'] != request.path:
                continue
            if dr['query'] != query:
                continue
            if dr['body'] != body:
                continue
            r = dr['response']
            dr['received_requests'] = dr['received_requests'] + 1
            break

        string_headers = {str(key): str(value) for key, value in r['headers'].iteritems()}

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

    def _run_post_interaction(self, request):
        interaction = from_json(request.body.read())

        pact_request = interaction['request']
        pact_response = interaction['response']

        path = pact_request['path']
        method = pact_request['method'].upper()
        methods = []
        description = interaction['description']
        provider_state = interaction['provider_state']

        query = pact_request.get('query', 'no_query_string')
        body = pact_request.get('body', 'no_body')

        pact_response.setdefault('headers', {})
        pact_response.setdefault('status', 200)
        pact_response.setdefault('body', '')

        if not len(self.dynamic_routes):
            self.append_route(description, provider_state, method, path, query, body, pact_response)
        else:
            match = False
            for dr in self.dynamic_routes:
                if (dr['description'] == description and dr['provider_state'] == provider_state and
                        dr['method'] == method and dr['path'] == path and dr['query'] == query and
                        dr['body'] == body and dr['response'] == pact_response):
                    dr['expected_requests'] = dr['expected_requests'] + 1
                    match = True
                    break
            if not match:
                self.append_route(description, provider_state, method, path, query, body, pact_response)

        methods = [r.get('method') for r in self.dynamic_routes if r.get('path') == path]

        self._app.route(path, methods, self.dynamic_route)

        self.registered_interactions.update(interaction)

        return 'Processed Interactions'

    def _run_delete_interaction(self):
        routes_to_clear = deepcopy(self._app.routes)

        for _route in routes_to_clear:
            if _route.rule != '/interactions':
                self._app.route(_route.rule, _route.method, self.clear_route)

        self.registered_interactions = {}
        return 'Cleared Interactions'

    def _interactions(self):
        verb = request.method.lower()

        if verb == 'post':
            return self._run_post_interaction(request)
        elif verb == 'delete':
            return self._run_delete_interaction()

    def _verification(self):
        vr = VerificationResults()

        def is_mismatch(row): return row.get('expected_requests') != row.get('received_requests')

        mismatched_interactions = [dr for dr in self.dynamic_routes if is_mismatch(dr)]

        if not len(mismatched_interactions):
            return vr.VerificationPassed()
        else:
            return vr.VerificationFailed(mismatched_interactions)
