from tests.mocks import *
import unittest


class TestClassForDotaApiParser(unittest.TestCase):
    test_data = read_test_data()

    def test_get_top_players_type(self):
        result = mock_top_players_response(1)
        assert type(result) == list

    def test_get_top_players_player(self):
        result = mock_top_players_response(1)
        assert (
            result == self.test_data["responses"]["top_players"]["assert_player_dict"]
        )

    def test_get_top_players_length(self):
        result = len(mock_top_players_response(50))
        assert result == 50

    def test_get_top_players_max_length(self):
        result = len(mock_top_players_response(500))
        assert result == self.test_data["responses"]["top_players"]["max_length"]

    def test_get_top_players_with_zero_response(self):
        result = len(mock_top_players_response(0))
        assert result == 0

    def test_get_recent_matches_for_player_type(self):
        result = mock_recent_matches_for_player_response()
        assert type(result) == list

    def test_get_recent_matches_for_player_response(self):
        result = mock_recent_matches_for_player_response()[0]
        assert (
            result
            == self.test_data["responses"]["recent_matches"][
                "assert_recent_matches_first_match"
            ]
        )

    def test_get_recent_matches_for_player_max_length(self):
        result = len(mock_recent_matches_for_player_response())
        assert result == self.test_data["responses"]["recent_matches"]["max_length"]

    def test_get_player_score_for_matches_keys(self):
        result = list(mock_player_score_for_matches_response().keys())
        assert (
            result
            == self.test_data["responses"]["player_score_for_matches"][
                "assert_player_matches_data_keys"
            ]
        )

    def test_get_player_score_for_matches_data_length(self):
        result = len(mock_player_score_for_matches_response()["kills"])
        assert (
            result
            == self.test_data["responses"]["player_score_for_matches"][
                "assert_kills_list_length"
            ]
        )

    def test_construct_player_data_keys(self):
        result = list(
            mock_construct_player_data(
                self.test_data["player_data"]["valid_no_zero_player_matches_data"]
            ).keys()
        )
        assert result == self.test_data["player_data"]["assert_keys"]

    def test_construct_player_data_fields(self):
        data = mock_construct_player_data(
            self.test_data["player_data"]["valid_no_zero_player_matches_data"]
        )
        result = [data["max_KDA"], data["max_KP"]]
        assert result[0] > 0 and result[1] > 0

    def test_construct_player_data_fields_neg(self):
        data = mock_construct_player_data(
            self.test_data["player_data"]["empty_player_matches_data"]
        )
        result = [data["max_KDA"], data["max_KP"]]
        assert result[0] == 0 and result[1] == 0
