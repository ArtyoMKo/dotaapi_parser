# pylint: disable=method-hidden,protected-access
import argparse
from unittest.mock import Mock, patch

from src.parser import DotaApiParser
from src.helpers import console_parser, request_template
from tests.helpers import read_test_data


class MockedResponseData:
    def __init__(self, status_code=200, reason="OK", content=None):
        if content is None:
            content = {"mocked_data": True}
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

    api = DotaApiParser(count)
    with patch("src.parser.request_template") as patched_request_template:
        patched_request_template.return_value = test_data["responses"]["top_players"][
            "response"
        ]
        return api._DotaApiParser__get_top_players()


def mock_recent_matches_for_player_response():
    test_data = read_test_data()

    api = DotaApiParser()
    with patch("src.parser.request_template") as patched_request_template:
        patched_request_template.return_value = test_data["responses"][
            "recent_matches"
        ]["response"]
        return api._DotaApiParser__get_recent_matches_for_player(
            test_data["responses"]["recent_matches"]["account_id"]
        )


def mock_player_score_for_matches_response():
    test_data = read_test_data()

    api = DotaApiParser()
    with patch("src.parser.request_template") as patched_request_template:
        patched_request_template.return_value = test_data["responses"][
            "player_score_for_matches"
        ]["response"]
        return api._DotaApiParser__get_player_score_for_matches(
            test_data["responses"]["player_score_for_matches"]["match_ids"],
            test_data["responses"]["player_score_for_matches"]["player_id"],
        )


def mock_construct_player_data(player_data):
    api = DotaApiParser()
    return api._DotaApiParser__construct_player_data(player_data)


def mock_console_parser(count):
    parser = argparse.ArgumentParser(
        description="Input one integer for parsing data count, defaults 10"
    )
    parser.add_argument(
        "--count", metavar="N", type=int, default=10, help="count of players"
    )
    with patch(
        "argparse.ArgumentParser.parse_args",
        return_value=argparse.Namespace(count=count),
    ):
        result = console_parser(parser)
    return result


def mock_console_parser_exception_neg():
    parser = argparse.ArgumentParser(
        description="Input one integer for parsing data count, defaults 10"
    )
    parser.add_argument(
        "--count", metavar="N", type=int, default=10, help="count of players"
    )
    with patch(
        "argparse.ArgumentParser.parse_args",
        side_effect=argparse.ArgumentError(None, "Wrong argument"),
    ):
        console_parser(parser)


def mock_template_request_for_log(url, side_effect):
    mock_requests = Mock()
    mock_requests.get.side_effect = side_effect
    request_template(url, mock_requests)
