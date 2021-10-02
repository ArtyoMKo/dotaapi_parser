import logging
import requests

from .helpers import request_template, compute_kda, compute_kp, construct_player_data_helper

TOP_PLAYERS_ENDPOINT = 'https://api.opendota.com/api/playersByRank'
PLAYER_MATCHES_ENDPOINT = "https://api.opendota.com/api/players/{}/recentMatches"
MATCH_DETAILS_ENDPOINT = "https://api.opendota.com/api/matches/{}"

class DotaApi:
    def __init__(self):
        self.top_players = []
        self.data = {
            'description': 'Parsed top players data from Dota game',
            'successfully': False,
            'message': '',
            'data': []
        }

    def __get_top_players(self, count):
        response = request_template(TOP_PLAYERS_ENDPOINT, requests)
        if response is not None or len(response) > 0:
            self.top_players = response[:count]
        return self.top_players

    def __get_recent_matches_for_player(self, player_id):
        response = request_template(PLAYER_MATCHES_ENDPOINT.format(player_id))
        match_ids = []
        if response is not None:
            for match in response:
                match_ids.append(match['match_id'])
        return match_ids

    def __get_player_score_for_matches(self, match_ids, player_id):
        player_matches_data = {
                'player_id': player_id,
                'total_games': len(match_ids),
                'kills': [],
                'deaths': [],
                'assists': [],
                'team_kills': [],
                'KDA': [],
                'KP': [],
            }
        for match_id in match_ids:
            response = request_template(MATCH_DETAILS_ENDPOINT.format(match_id))
            if response is not None:
                for player in response['players']:
                    if player['account_id'] == player_id:
                        if player['isRadiant']:
                            team_kills = response['radiant_score']
                        else:
                            team_kills = response['dire_score']
                        player_matches_data['kills'].append(player['kills'])
                        player_matches_data['deaths'].append(player['deaths'])
                        player_matches_data['assists'].append(player['assists'])
                        player_matches_data['team_kills'].append(team_kills)
                        player_matches_data['KDA'].append(compute_kda(
                            player['kills'],
                            player['deaths'],
                            player['assists']
                        ))
                        player_matches_data['KP'].append(compute_kp(
                            player['kills'],
                            player['deaths'],
                            team_kills
                        ))
                        break
        return player_matches_data

    def __construct_player_data(self, player_matches_data):
        return construct_player_data_helper(player_matches_data)

    def parse_top_players_and_their_data(self, count):
        self.__get_top_players(count)
        if len(self.top_players):
            for player in self.top_players:
                match_ids = self.__get_recent_matches_for_player(player['account_id'])
                if len(match_ids):
                    player_matches_data = self.__get_player_score_for_matches(match_ids, player['account_id'])
                    player_finale_data = self.__construct_player_data(player_matches_data)
                    self.data['data'].append(player_finale_data)
                else:
                    self.data['message'] = 'Match ids does not exists for some account(s)'
            self.data['successfully'] = True
        else:
            self.data['message'] = 'Top players does not exists, see logs.log messages'
        return self.data



