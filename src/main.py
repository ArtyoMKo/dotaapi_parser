from helpers import console_parser
from tools import DotaApi
import logging


def main():
    logging.basicConfig(filename="logs.log", level=logging.INFO)


if __name__ == '__main__':
    argument = console_parser()
    print(argument)
