from typing import List, Dict, Union
from datetime import datetime
import time
import requests

from src.helpers import read_json as read_messages
from src.helpers import (
    request_template,
    compute_kda,
    compute_kp,
    construct_player_data_helper,
)

TOP_PLAYERS_ENDPOINT = "https://api.opendota.com/api/playersByRank"
PLAYER_MATCHES_ENDPOINT = "https://api.opendota.com/api/players/{}/recentMatches"
MATCH_DETAILS_ENDPOINT = "https://api.opendota.com/api/matches/{}"


class DotaApiParser:
    def __init__(
        self,
        count: int = 10,
        start_date_date: datetime = datetime.now(),
        timeout: int = 2,
    ):
        self.top_players: List = []
        self.data: Dict = {
            "description": "Parsed top players data from Dota game",
            "successfully": False,
            "message": "",
            "parsed_data": start_date_date,
            "parsing_time_sec": "",
            "data": [],
        }
        self.start_time: float = time.time()
        self.timeout: int = timeout
        self.count: int = count

    def __get_top_players(self) -> List:
        response = request_template(TOP_PLAYERS_ENDPOINT, requests)
        if response is not None:
            if isinstance(response, list) and len(response) > 0:
                self.top_players = response[: self.count]
        return self.top_players

    def __get_recent_matches_for_player(
        self, player_id: Union[str, int]
    ) -> List[Union[str, int]]:
        response = request_template(PLAYER_MATCHES_ENDPOINT.format(player_id))
        match_ids = []
        if response is not None:
            for match in response:
                match_ids.append(match["match_id"])
        return match_ids

    def __get_player_score_for_matches(
        self, match_ids: List[Union[str, int]], player_id: Union[str, int]
    ) -> Dict:
        player_matches_data: Dict = {
            "player_id": player_id,
            "total_games": len(match_ids),
            "kills": [],
            "deaths": [],
            "assists": [],
            "team_kills": [],
            "KDA": [],
            "KP": [],
        }
        for match_id in match_ids:
            response = request_template(MATCH_DETAILS_ENDPOINT.format(match_id))
            if response is not None:
                for player in response["players"]:
                    if player["account_id"] == player_id:
                        if player["isRadiant"]:
                            team_kills = response["radiant_score"]
                        else:
                            team_kills = response["dire_score"]
                        player_matches_data["kills"].append(player["kills"])
                        player_matches_data["deaths"].append(player["deaths"])
                        player_matches_data["assists"].append(player["assists"])
                        player_matches_data["team_kills"].append(team_kills)
                        player_matches_data["KDA"].append(
                            compute_kda(
                                player["kills"], player["deaths"], player["assists"]
                            )
                        )
                        player_matches_data["KP"].append(
                            compute_kp(player["kills"], player["deaths"], team_kills)
                        )
                        break
        return player_matches_data

    def __construct_player_data(self, player_matches_data: Dict) -> Dict:
        return construct_player_data_helper(player_matches_data)

    def parse_top_players_and_their_data(self) -> Dict:
        messages = read_messages("src/messages.json")
        self.__get_top_players()
        if self.top_players:
            for player in self.top_players:
                time.sleep(self.timeout)
                match_ids = self.__get_recent_matches_for_player(player["account_id"])
                if match_ids:
                    time.sleep(self.timeout)
                    player_matches_data = self.__get_player_score_for_matches(
                        match_ids, player["account_id"]
                    )
                    time.sleep(self.timeout)
                    player_finale_data = self.__construct_player_data(
                        player_matches_data
                    )
                    self.data["data"].append(player_finale_data)
                else:
                    self.data["message"] = messages["api"]["no_match_ids"]
            self.data["successfully"] = True
            self.data["message"] = messages["api"]["success"]
        else:
            self.data["message"] = messages["api"]["no_players"]
        self.data["parsing_time_sec"] = str(round(time.time() - self.start_time, 2))
        return self.data
