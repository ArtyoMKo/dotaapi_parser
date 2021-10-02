import requests
import logging

def console_parser(parser):
    argument = parser.parse_args().count
    if argument > 100:
        argument = 100
        logging.info("allowed count in range of 0-100")
    elif argument < 0:
        argument = 1
        logging.info("allowed count in range of 0-100, with negative count will set 1")
    return argument

def compute_kda(kills, deaths, assists):
    kd = kills+deaths
    if assists == 0:
        return round(kd, 2)
    else:
        return round(kd/assists, 2)

def compute_kp(kills, deaths, team_kills):
    kd = kills + deaths
    if team_kills == 0:
        return 0
    else:
        return round(kd*100/team_kills, 2)

def compute_avg(array):
    try:
        return round(sum(array)/len(array), 2)
    except ZeroDivisionError:
        return 0

def request_template(endpoint, user_agent=requests):
    response_for_return = None
    try:
        response = user_agent.get(endpoint)
        if response.status_code != 200:
            logging.error(f"Request to {endpoint} endpoint finished with {response.status_code} code with \
            {response.reason} reason")
        else:
            response_for_return = response.json()
    except user_agent.exceptions.ConnectionError:
        logging.error("Internet Connection error")
    except user_agent.exceptions.Timeout:
        logging.error("Connection timeout")
    except user_agent.exceptions.MissingSchema:
        logging.error("URL does not exist")
    except:
        logging.error("Unknown problem with requesting or DotaAPI")
    finally:
        return response_for_return

def construct_player_data_helper(player_matches_data):
    try:
        return {
            'game': 'Dota',
            'player_id': player_matches_data['player_id'],
            'max_KDA': max(player_matches_data['KDA']),
            'min_KDA': min(player_matches_data['KDA']),
            'avg_KDA': compute_avg(player_matches_data['KDA']),
            'max_KP': max(player_matches_data['KDA']),
            'min_KP': min(player_matches_data['KDA']),
            'avg_KP': compute_avg(player_matches_data['KP'])
        }
    except ValueError:
        logging.error(f"API ERROR:Empty data for {player_matches_data['player_id']}")
        return {
            'game': 'Dota',
            'player_id': player_matches_data['player_id'],
            'max_KDA': 0,
            'min_KDA': 0,
            'avg_KDA': 0,
            'max_KP': 0,
            'min_KP': 0,
            'avg_KP': 0
        }



