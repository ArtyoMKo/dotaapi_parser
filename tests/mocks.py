from unittest.mock import Mock

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
