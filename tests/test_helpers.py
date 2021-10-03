from src.helpers import *
from src.parser import *
from tests.mocks import *

import unittest
from pytest import raises

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

    def test_console_parser_exception(self):
        with raises(argparse.ArgumentError):
            mock_console_parser_exception()

    def test_read_json_test_data(self):
        result = read_json('tests/test_data.json')
        assert result == self.test_data

    def test_save_parsed_data(self):
        parsed_data = {'data': 'empty_data'}
        save_parsed_data(parsed_data)
        result = read_json('parsed_data.json')
        assert result == parsed_data


class TestLogs(unittest.TestCase):
    messages = read_test_data()

    def test_request_template_connection_error_log(self):
        with self.assertLogs() as captured:
            mock_template_request_for_log(
                'https://api.opendota.com/api/playersByRank',
                requests.exceptions.ConnectionError
            )
        assert captured.records[0].getMessage() == self.messages['messages']['response']['connection_error']

    def test_request_template_timeout_log(self):
        with self.assertLogs() as captured:
            mock_template_request_for_log(
                'https://api.opendota.com/api/playersByRank',
                requests.exceptions.Timeout
            )
        assert captured.records[0].getMessage() == self.messages['messages']['response']['timeout']

    def test_request_template_missing_schema_log(self):
        with self.assertLogs() as captured:
            mock_template_request_for_log(
                '',
                requests.exceptions.MissingSchema
            )
        assert captured.records[0].getMessage() == self.messages['messages']['response']['missing_schema']

    def test_request_template_unknown_error_log(self):
        with self.assertLogs() as captured:
            mock_template_request_for_log(
                'https://api.opendota.com/api/playersByRank',
                'Unknown exception'
            )
        assert captured.records[0].getMessage() == self.messages['messages']['response']['unknown_exception']

    def test_console_parser_neg_log(self):
        with self.assertLogs() as captured:
            mock_console_parser(-10)
        assert captured.records[0].getMessage() == self.messages['messages']['console']['negative']

    def test_console_parser_log(self):
        with self.assertLogs() as captured:
            mock_console_parser(1000)
        assert captured.records[0].getMessage() == self.messages['messages']['console']['hug']
