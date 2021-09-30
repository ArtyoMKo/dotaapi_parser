import logging
import requests

from .helpers import request_template, compute_kda, compute_kp, compute_avg


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


class Logger:
    def __init__(self):
        self.logger = logging
        # self.logger.basicConfig(filename="logs.log", level=logging.INFO)

    def debug(self, message):
        logging.debug(message)

    def info(self, message):
        logging.info(message)

    def error(self, message):
        logging.error(message)


class DotaApi:
    def __init__(self):
        self.top_players = []
        self.data = {
            'description': 'Parsed top players data from Dota game',
            'data': []
        }
        self.top_players_endpoint = 'https://api.opendota.com/api/playersByRank'
        self.player_matches_endpoint = "https://api.opendota.com/api/players/{}/recentMatches"
        self.match_details_endpoint = "https://api.opendota.com/api/matches/{}"

    def __get_top_players(self, count):
        response = request_template(self.top_players_endpoint, requests)
        if response is not None:
            self.top_players = response[:count]
        return self.top_players

    def __get_recent_matches_for_player(self, player_id):
        response = request_template(self.player_matches_endpoint.format(player_id))
        match_ids = []
        if response is not None:
            for match in response:
                match_ids.append(match['match_id'])
        return match_ids

    def __get_player_score_for_matches(self, match_ids, player_id):
        player_matches_data = {
                'player_name': '',
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
            response = request_template(self.match_details_endpoint.format(match_id))
            if response is not None:
                for player in response['players']:
                    if player['account_id'] == player_id:
                        if player['account_id']['isRadiant']:
                            team_kills = response['radiant_score']
                        else:
                            team_kills = response['dire_score']
                        player_matches_data['kills'].append(player['account_id']['kills'])
                        player_matches_data['deaths'].append(player['account_id']['deaths'])
                        player_matches_data['assists'].append(player['account_id']['assists'])
                        player_matches_data['team_kills'].append(team_kills)
                        player_matches_data['KDA'].append(compute_kda(
                            player['account_id']['kills'],
                            player['account_id']['deaths'],
                            player['account_id']['assists']
                        ))
                        player_matches_data['KP'].append(compute_kp(
                            player['account_id']['kills'],
                            player['account_id']['deaths'],
                            team_kills
                        ))
                        break
        if len(match_ids):
            player_matches_data['player_name'] = player['account_id']['personaname']
        return player_matches_data

    def __construct_player_data(self, player_matches_data):
        return {
            'game': 'Dota',
            'player_name': player_matches_data['player_name'],
            'player_id': player_matches_data['player_id'],
            'max_KDA': max(player_matches_data['KDA']),
            'min_KDA': min(player_matches_data['KDA']),
            'avg_KDA': compute_avg(player_matches_data['KDA']),
            'max_KP': max(player_matches_data['KDA']),
            'min_KP': min(player_matches_data['KDA']),
            'avg_KP': compute_avg(player_matches_data['KP'])
        }

    def parse_top_players_and_their_data(self, count):
        self.__get_top_players(count)
        if len(self.top_players):
            for player in self.top_players:
                match_ids = self.__get_recent_matches_for_player(player['account_id'])
                if len(match_ids):
                    player_matches_data = self.__get_player_score_for_matches(match_ids, player['account_id'])
                    player_finale_data = self.__construct_player_data(player_matches_data)
                    self.data['data'].append(player_finale_data)
        return self.data

