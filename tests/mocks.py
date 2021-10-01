from unittest.mock import Mock, patch

from src import DotaApi
from tests.helpers import read_test_data


class MockedResponseData:
    def __init__(self, status_code=200, reason='OK', content=None):
        if content is None:
            content = {'mocked_data': True}
        self.content = content
        self.status_code = status_code
        self.reason = reason

    def json(self):
        return self.content

    def status_code(self):
        return self.status_code

    def reason(self):
        return self.reason

def mock_get_request(return_value=MockedResponseData(), side_effect=None):
    mock_requests = Mock()
    if side_effect:
        mock_requests.get.side_effect = side_effect
    else:
        mock_requests.get.return_value = return_value
    return mock_requests

def mock_top_players_response(count):
    test_data = read_test_data()

    api = DotaApi()
    with patch('src.tools.request_template') as patched_request_template:
        patched_request_template.return_value = test_data['responses']['top_players']['response']
        return api._DotaApi__get_top_players(count)

def mock_recent_matches_for_player_response():
    test_data = read_test_data()

    api = DotaApi()
    with patch('src.tools.request_template') as patched_request_template:
        patched_request_template.return_value = test_data['responses']['recent_matches']['response']
        return api._DotaApi__get_recent_matches_for_player(test_data['responses']['recent_matches']['account_id'])
