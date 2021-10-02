import argparse
import logging
import datetime
import time

from helpers import console_parser


def main(parser):
    start_time = time.time()
    logging.basicConfig(filename="logs.log", filemode='w', level=logging.INFO)
    argument = console_parser(parser)
    logging.info(f"{str(datetime.datetime.now())}: Session started, parsing {argument} accounts")
    end_time = time.time()
    logging.info(f"{str(datetime.datetime.now())}: Session ended, execution time |->> {round(end_time-start_time, 8)} "
                 f"seconds")
    logging.shutdown()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Input one integer for parsing data count, defaults 10')
    parser.add_argument('count', metavar='N', type=int, default=10, help='count of players')
    main(parser)
