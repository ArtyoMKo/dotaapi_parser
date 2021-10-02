import argparse
import logging
import datetime
import time

from src.parser import DotaApi
from src.helpers import console_parser, save_json


def main(parser):
    start_time = time.time()
    start_date = str(datetime.datetime.now())
    
    logging.basicConfig(filename="src/logs.log", filemode='w', level=logging.INFO)

    players_count = console_parser(parser)
    logging.info(f"{start_date}: Session started, parsing {players_count} accounts")

    dota_api = DotaApi(players_count, start_date)
    parsed_data = dota_api.parse_top_players_and_their_data()
    save_json(parsed_data)

    end_time = time.time()
    logging.info(f"{str(datetime.datetime.now())}: Session ended, execution time |->> {round(end_time-start_time, 8)} "
                 f"seconds")
    logging.shutdown()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Input one integer for parsing data count, defaults 10')
    parser.add_argument('count', metavar='N', type=int, default=10, help='count of players')
    main(parser)
