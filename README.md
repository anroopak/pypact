# pypact

*Warning: currently a stub, nothing currently implemented!*

**pypact** is a [consumer driven contract
testing](http://martinfowler.com/articles/consumerDrivenContracts.html) library
that allows mocking of responses in the consumer codebase, and verification of
the interaction in the provider codebase.

**pypact** is an implementation of the [Pact Specification
(v1.1)](https://github.com/bethesque/pact-specification).

## CI Status

[![travis-ci.org Build Status](https://travis-ci.org/hartror/pypact.png)](https://travis-ci.org/hartror/pypact)
[![Coverage Status](https://coveralls.io/repos/hartror/pypact/badge.svg)](https://coveralls.io/r/hartror/pypact)

## How to use

### 1. Configure Pact

```python
def mock_server(consumer, provider, port, path):
    if os.path.exists(path):
        shutil.rmtree(path)
    else:
        os.makedirs(path)

    consumer = pypact.Consumer(consumer)
    provider = pypact.Provider(provider)
    server = consumer.has_pact_with(provider, port)

    return server

def main(argv=None):
    consumer = "My consumer"
    provider = "My provider"
    port = "1234"
    path = "./pacts"

    server = mock_server(consumer, provider, port, path)
```

### 2. Start the mock server

```python
def start_server():
    pypact.MockServer()

def main(argv=None):
    // Configure pact

    p = Process(target=start_server)
    p.daemon = True
    p.start()
    time.sleep(3)

    // Other steps

    p.terminate()
```

### 3. Register the interaction

```python
def register_interaction(interaction, url, action):
    client = pypact.MockServerClient(url)
    if action == "post":
        result = client.post_interaction(interaction.to_JSON())

    return result

def main(argv=None):
    // Configure pact
    // Start the mock server

    interaction = (server
        .given("There is a user wih id {23}")
        .upon_receiving("get request for user with id {23}")
        .with_request(method="GET", path="/user", query="id=23")
        .will_respond_with(
            status=200,
            headers={"Content-Type": "application/json"},
            body={"firstName": "John"}
        )
    )

    url = "http://localhost:8080"
    action = "post"

    result = register_interaction(interaction, url, action)
```

### 4. Hit the endpoint

```python
def main(argv=None):
    // Configure pact
    // Start the mock server
    // Register interaction

    name = requests.get('http://localhost:8080/user?id=23')
```

### 5. Run the tests

```bash
$ python pypact/test/test_end2end.py
```
