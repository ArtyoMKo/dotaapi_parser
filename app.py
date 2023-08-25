import argparse
import logging
import datetime
import time
import threading
from flask import Flask

from src.parser import DotaApiParser
from src.helpers import console_parser
from src.helpers import read_json as read_saved_data
from src.helpers import save_json as save_parsed_data

app = Flask(__name__)
PARSER = argparse.ArgumentParser(
    description="Input one integer for parsing data count, defaults 10"
)
PARSER.add_argument(
    "--count", metavar="N", type=int, default=10, help="count of players"
)


@app.route("/")
def get_log():
    with open("src/logs.log", "r", encoding="utf=8") as read_file:
        data = read_file.read().splitlines()
    return {"logs": data}


@app.route("/saved_data")
def get_saved_data():
    return read_saved_data("parsed_data.json")


def pars_data(
    players_number: int, start_time_sec: int, start_date_date: datetime.datetime
) -> None:
    dota_api = DotaApiParser(players_number, start_date_date)
    parsed_data = dota_api.parse_top_players_and_their_data()
    save_parsed_data(parsed_data)

    end_time = time.time()
    logging.info(
        f"{str(datetime.datetime.now())}: Session ended"
        f" execution time |->> {round(end_time-start_time_sec, 8)} "
        f"seconds"
    )


if __name__ == "__main__":
    start_time = time.time()
    START_DATE = str(datetime.datetime.now())
    players_count = console_parser(PARSER)

    logging.basicConfig(filename="src/logs.log", filemode="w", level=logging.INFO)
    logging.info(
        f"{START_DATE}: Session started, "
        f"parsing {players_count} accounts, please wait until session ending"
    )

    save_parsed_data({})

    parser_thread = threading.Thread(
        target=pars_data,
        name="Data parser",
        args=([players_count, start_time, START_DATE]),
    )
    parser_thread.start()

    app.run(host="0.0.0.0", port=5000)
