from typing import Dict, List, Union
from argparse import ArgumentError, ArgumentParser
import logging
import json
import requests


def console_parser(parser: ArgumentParser) -> int:
    messages = read_json("src/messages.json")
    try:
        argument = parser.parse_args().count
        if argument > 100:
            argument = 100
            logging.info(messages["console"]["hug"])
        elif argument < 0:
            argument = 1
            logging.info(messages["console"]["negative"])
        return argument
    except ArgumentError:
        logging.error("console argument error")
        raise ArgumentError(None, "Wrong argument")


def compute_kda(kills: int, deaths: int, assists: int) -> float:
    kd_metric = kills + deaths
    if assists == 0:
        return round(kd_metric, 2)
    return round(kd_metric / assists, 2)


def compute_kp(kills: int, deaths: int, team_kills: int) -> float:
    kd_metric = kills + deaths
    if team_kills == 0:
        return 0
    return round(kd_metric * 100 / team_kills, 2)


def compute_avg(array: List[Union[int, float]]) -> Union[float, int]:
    try:
        return round(sum(array) / len(array), 2)
    except ZeroDivisionError:
        return 0


def request_template(endpoint: str, user_agent=requests) -> Union[Dict, None]:
    messages = read_json("src/messages.json")
    response_for_return = None
    try:
        response = user_agent.get(endpoint)
        if response.status_code != 200:
            logging.error(
                f"Request to {endpoint} endpoint finished with {response.status_code} code with "
                f"{response.reason} reason"
            )
        else:
            response_for_return = response.json()
    except requests.exceptions.ConnectionError:
        logging.error(messages["response"]["connection_error"])
    except requests.exceptions.Timeout:
        logging.error(messages["response"]["timeout"])
    except requests.exceptions.MissingSchema:
        logging.error(messages["response"]["missing_schema"])
    except:  # pylint: disable=bare-except
        logging.error(messages["response"]["unknown_exception"])
    return response_for_return


def construct_player_data_helper(player_matches_data: Dict) -> Dict:
    try:
        return {
            "game": "Dota",
            "player_id": player_matches_data["player_id"],
            "max_KDA": max(player_matches_data["KDA"]),
            "min_KDA": min(player_matches_data["KDA"]),
            "avg_KDA": compute_avg(player_matches_data["KDA"]),
            "max_KP": max(player_matches_data["KDA"]),
            "min_KP": min(player_matches_data["KDA"]),
            "avg_KP": compute_avg(player_matches_data["KP"]),
        }
    except ValueError:
        logging.error(f"API ERROR:Empty data for {player_matches_data['player_id']}")
        return {
            "game": "Dota",
            "player_id": player_matches_data["player_id"],
            "max_KDA": 0,
            "min_KDA": 0,
            "avg_KDA": 0,
            "max_KP": 0,
            "min_KP": 0,
            "avg_KP": 0,
        }


def read_json(source: str):
    try:
        with open(source, "r", encoding="utf-8") as read_file:
            data = json.load(read_file)
        return data
    except FileNotFoundError:
        logging.error(f"{source} file not found")
        raise FileNotFoundError


def save_json(
    parsed_data: Union[Dict, List, str, bytes], source: str = "parsed_data.json"
):
    with open(source, "w", encoding="utf-8") as write_file:
        json.dump(parsed_data, write_file, ensure_ascii=False, indent=4)
