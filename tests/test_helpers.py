from src import *
from .mocks import *
import unittest

class TestClassForHelperMethods(unittest.TestCase):
    test_data = read_test_data()

    def test_request_template(self):
        mock_requests = mock_get_request(return_value=MockedResponseData())
        assert request_template('https://api.opendota.com/api/playersByRank', mock_requests)['mocked_data']\
               is self.test_data['mocked_data']

    def test_request_template_neg_connection_error(self):
        mock_requests = mock_get_request(side_effect=requests.exceptions.ConnectionError)
        assert request_template("https://api.opendota.com/api/playersByRank", mock_requests) is None

    def test_request_template_neg_timeout(self):
        mock_requests = mock_get_request(side_effect=requests.exceptions.Timeout)
        assert request_template("https://api.opendota.com/api/playersByRank", mock_requests) is None

    def test_request_template_neg_missing_schema(self):
        mock_requests = mock_get_request(side_effect=requests.exceptions.MissingSchema)
        assert request_template("https://api.opendota.com/api/playersByRank", mock_requests) is None

    def test_request_template_neg_invalid_url(self):
        mock_requests = mock_get_request(side_effect=requests.exceptions.MissingSchema)
        assert request_template('InvalidURL', mock_requests) is None

    def test_compute_kda(self):
        kda = compute_kda(
            self.test_data['kills'], self.test_data['deaths'], self.test_data['assists']
        )
        assert kda == self.test_data['kda']

    def test_compute_kda_neg(self):
        kda = compute_kda(
            self.test_data['kills'], self.test_data['deaths'], self.test_data['assists_neg']
        )
        assert kda == self.test_data['kda_neg']

    def test_compute_kp(self):
        kp = compute_kp(
            self.test_data['kills'], self.test_data['deaths'], self.test_data['team_kills']
        )
        assert kp == self.test_data['kp']

    def test_compute_kp_neg(self):
        kp = compute_kp(
            self.test_data['kills'], self.test_data['deaths'], self.test_data['team_kills_neg']
        )
        assert kp == self.test_data['kp_neg']

    def test_compute_avg(self):
        avg = compute_avg(
            self.test_data['avg_array']
        )
        assert avg == self.test_data['avg']

    def test_compute_avg_neg(self):
        avg = compute_avg(
            self.test_data['avg_array_neg']
        )
        assert avg == self.test_data['avg_neg']

    def test_console_parser(self):
        result = mock_console_parser(10)
        assert result == 10

    def test_console_parser_neg(self):
        result = mock_console_parser(-10)
        assert result == 1

    def test_console_parser_hug(self):
        result = mock_console_parser(1000)
        assert result == 100

# def test_request_template_neg_timeout_log(caplog):
#     from unittest.mock import Mock
#     mock_requests = Mock()
#     mock_requests.get.side_effect = requests.exceptions.Timeout
#     request_template('ValidURL', mock_requests)
#     assert 'timeout' in caplog.text


# class CaptureLogsExample(unittest.TestCase):
#     @loggingtestcase.capturelogs('root', level='ERROR')
#     def test_always_display_logs(self, logs):
#         from unittest.mock import Mock
#         mock_requests = Mock()
#         mock_requests.get.side_effect = requests.exceptions.ConnectionError
#         # logging.getLogger('root').error('Internet Connection error')
#         request_template('ValidURL', mock_requests)
#         self.assertEqual(logs.output, ['ERROR:root:Internet Connection error'])
