import requests
import logging
import sys
import json

def console_parser():
    arguments = sys.argv
    arg = 10
    if len(arguments) > 1:
        if arguments[1].isdigit():
            parsed_argument = int(arguments[1])
            if parsed_argument > 100:
                arg = 100
                logging.info("allowed count in range of 0-100")
            else:
                arg = parsed_argument
        else:
            logging.error("inputted not digit argument (string or with minus)")
    return arg

def compute_kda(kills, deaths, assists):
    return round((kills+deaths)/assists, 2)

def compute_kp(kills, deaths, team_kills):
    return round((kills+deaths)*100/team_kills, 2)

def compute_avg(array):
    return round(sum(array)/len(array), 2)

def read_test_data():
    with open('test_data.json', 'r') as rf:
        data = json.load(rf)
    return data

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
