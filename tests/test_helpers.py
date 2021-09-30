from src import *
from src import MockedResponseData


class TestClassForHelperMethods:
    test_data = read_test_data()

    def test_request_template(self):
        from unittest.mock import Mock
        mock_requests = Mock()
        mock_requests.get.return_value = MockedResponseData()
        assert request_template('ValidURL', mock_requests)['mocked_data'] is self.test_data['mocked_data']

    def test_request_template_neg_connection_error(self):
        from unittest.mock import Mock
        mock_requests = Mock()
        mock_requests.get.side_effect = requests.exceptions.ConnectionError
        assert request_template("https://api.opendota.com/api/playersByRank", mock_requests) is None

    def test_request_template_neg_timeout(self):
        from unittest.mock import Mock
        mock_requests = Mock()
        mock_requests.get.side_effect = requests.exceptions.Timeout
        assert request_template("https://api.opendota.com/api/playersByRank", mock_requests) is None

    def test_request_template_neg_missing_schema(self):
        from unittest.mock import Mock
        mock_requests = Mock()
        mock_requests.get.side_effect = requests.exceptions.MissingSchema
        assert request_template("https://api.opendota.com/api/playersByRank", mock_requests) is None

    def test_request_template_neg_invalid_url(self):
        from unittest.mock import Mock
        mock_requests = Mock()
        mock_requests.get.side_effect = requests.exceptions.MissingSchema
        assert request_template('InvalidURL', mock_requests) is None

    def test_compute_kda(self):
        assert compute_kda(
            self.test_data['kills'], self.test_data['deaths'], self.test_data['assists']
        ) == self.test_data['kda']

    def test_compute_kp(self):
        assert compute_kp(
            self.test_data['kills'], self.test_data['deaths'], self.test_data['team_kills']
        ) == self.test_data['kp']

    def test_compute_avg(self):
        assert compute_avg(
            self.test_data['avg_array']
        ) == self.test_data['avg']

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
