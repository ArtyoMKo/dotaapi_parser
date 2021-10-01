from src import *
from .helpers import *
from .mocks import *
import unittest
from unittest.mock import patch


class TestClassForDotaApi(unittest.TestCase):
    test_data = read_test_data()

    def test_get_top_players_type(self):
        result = mock_top_players_response(1)
        assert type(result) == list

    def test_get_top_players_player(self):
        result = mock_top_players_response(1)
        assert result == self.test_data['responses']['top_players']['assert_player_dict']

    def test_get_top_players_length(self):
        result = mock_top_players_response(50)
        assert len(result) == 50

    def test_get_top_players_max_length(self):
        result = mock_top_players_response(500)
        assert len(result) == self.test_data['responses']['top_players']['max_length']
    
    def test_get_top_players_with_zero_response(self):
        result = mock_top_players_response(0)
        assert len(result) == 0
        #
        # with patch.object(api, '_DotaApi__get_top_players', return_value={'hey': 123}) as method:
        #     # api.no_get_top_players()
        #     api.get_players(200)
        #     # method.assert_called_once_with()
        #     assert api.get_players(200) == {'hey': 123}
