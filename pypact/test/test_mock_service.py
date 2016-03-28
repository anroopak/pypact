import pytest
import pypact
import mock

@pytest.fixture
def mock_consumer():
    return mock.Mock()


@pytest.fixture
def mock_provider():
    return mock.Mock()


@pytest.fixture
def mock_interaction_builder():
    return mock.Mock()


@pytest.fixture
def mock_add_method():
    return mock.Mock()


def test_mock_service_creation(
        mock_consumer,
        mock_provider):

    service = pypact.MockService(
        consumer=mock_consumer,
        provider=mock_provider,
        port=1234)

    assert service.consumer == mock_consumer
    assert service.provider == mock_provider
    assert service.port == 1234


@pytest.fixture
def mock_service(mock_consumer, mock_provider):
    return pypact.MockService(
        consumer=mock_consumer,
        provider=mock_provider,
        port=1234)


def test_mock_service_is_stopped_on_creation(mock_service):
    assert mock_service.stopped


def test_mock_service_is_not_stopped_on_start(mock_service):
    mock_service.start()
    assert not mock_service.stopped


def test_mock_service_is_stopped_on_end(mock_service):
    mock_service.start()
    mock_service.end()
    assert mock_service.stopped


def test_mock_service_cannot_start_while_started(mock_service):
    mock_service.start()
    with pytest.raises(pypact.PyPactException):
        mock_service.start()


def test_mock_service_cannot_end_while_stopped(mock_service):
    with pytest.raises(pypact.PyPactException):
        mock_service.end()


def test_mock_service_starts_and_stops_with_with(mock_service):
    with mock_service:
        assert not mock_service.stopped
    assert mock_service.stopped


TEST_STATE = "an alligator exists"
TEST_DESCRIPTION = "a request for an alligator"


def test_interaction_builder_returns_interaction(mock_service, mock_add_method):
    interaction = mock_service.interaction_builder(mock_add_method)

    assert interaction.add_method == mock_add_method


def test_mock_service_returns_interaction_builder_on_given(
        mock_service):
    interaction_builder = mock.Mock()
    mock_service.interaction_builder = interaction_builder

    builder = mock_service.given(TEST_STATE)

    interaction_builder.assert_called_once_with(
        mock_service.add_interaction)

    assert builder == (
        interaction_builder()
        .given(TEST_STATE, mock_service.add_interaction))


def test_mock_service_returns_interaction_builder_on_upon_receiving(
        mock_service):
    interaction_builder = mock.Mock()
    mock_service.interaction_builder = interaction_builder

    builder = mock_service.upon_receiving(TEST_DESCRIPTION)

    interaction_builder.assert_called_once_with(
        mock_service.add_interaction)

    assert builder == (
        interaction_builder()
        .upon_receiving(TEST_DESCRIPTION, mock_service.add_interaction))


def test_mock_service_accepts_a_new_interaction(mock_service):
    mock_interaction = mock.Mock()
    mock_service.add_interaction(mock_interaction)
    assert len(mock_service.interactions) == 1
