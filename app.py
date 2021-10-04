from flask import Flask
import argparse
import logging
import datetime
import time
import threading

from src.parser import DotaApiParser
from src.helpers import console_parser
from src.helpers import read_json as read_saved_data
from src.helpers import save_json as save_parsed_data

app = Flask(__name__)
PARSER = argparse.ArgumentParser(description='Input one integer for parsing data count, defaults 10')
PARSER.add_argument('--count', metavar='N', type=int, default=10, help='count of players')

@app.route('/')
def get_log():
    with open('src/logs.log', 'r') as rf:
        data = rf.read().splitlines()
    return {
        'logs': data
    }

@app.route('/saved_data')
def get_saved_data():
    return read_saved_data('parsed_data.json')

def pars_data(players_count):
    start_time = time.time()
    start_date = str(datetime.datetime.now())
    
    logging.basicConfig(filename="src/logs.log", filemode='w', level=logging.INFO)

    logging.info(f"{start_date}: Session started, parsing {players_count} accounts, please wait until session ending")

    dota_api = DotaApiParser(players_count, start_date)
    parsed_data = dota_api.parse_top_players_and_their_data()
    save_parsed_data(parsed_data)

    end_time = time.time()
    logging.info(f"{str(datetime.datetime.now())}: Session ended, execution time |->> {round(end_time-start_time, 8)} "
                 f"seconds")
    logging.shutdown()


if __name__ == "__main__":
    save_parsed_data({})

    players_count = console_parser(PARSER)

    parser_thread = threading.Thread(
        target=pars_data, name='Data parser', args=([players_count])
    )
    parser_thread.start()

    app.run(host='0.0.0.0', port=5000)

