import logging

from src import request_template
from src import MockedResponseData


def test_request_template():
    from pytest import raises
    from unittest.mock import Mock
    mock_requests = Mock()
    mock_requests.get.return_value = MockedResponseData()
    logger = logging
    logger.basicConfig(filename="logs.log", level=logging.INFO)
    assert request_template('ValidURL', logger, mock_requests)['mocked_data'] == True
