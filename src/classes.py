import logging
from .helpers import request_template

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
        self.logger.basicConfig(filename="logs.log", level=logging.INFO)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def error(self, message):
        self.logger.error(message)


class DotaApi:
    def __init__(self):
        self.top_players = []
        self.data = []
        self.top_players_endpoint = 'https://api.opendota.com/api/playersByRank'
        self.player_matches_endpoint = "https://api.opendota.com/api/players/{}/recentMatches"
        self.match_details_endpoint = "https://api.opendota.com/api/matches/{}"
        self.own_logger = Logger()

    def get_top_players(self, count):
        response = request_template(self.top_players_endpoint, self.own_logger)
        if response is not None:
            self.top_players = response[:count]
        return self.top_players

    def __get_player_score_for_matches(self, match_ids, player_id):
        player_matches_data = []
        for match_id in match_ids:
            response = request_template(self.match_details_endpoint.format(match_id))
            if response is not None:
                for player in response['players']:
                    if player['account_id'] == player_id:
                        if player['account_id']['isRadiant']:
                            team_kills = response['radiant_score']
                        else:
                            team_kills = response['dire_score']
                        player_match_data = {
                            'kills': player['account_id']['kills'],
                            'deaths': player['account_id']['deaths'],
                            'assists': player['account_id']['assists'],
                            'personaname': player['account_id']['personaname'],
                            'team_kills': team_kills
                        }
                        player_matches_data.append(player_match_data)
                        break
        return player_matches_data

    def __get_recent_matches_for_player(self, player_id):
        response = request_template(self.player_matches_endpoint.format(player_id))
        match_ids = []
        if response is not None:
            for match in response:
                match_ids.append(match['match_id'])
