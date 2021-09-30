import requests
import sys

def console_parser(local_logger):
    arguments = sys.argv
    arg = 10
    if len(arguments) > 1:
        if arguments[1].isdigit():
            parsed_argument = int(arguments[1])
            if parsed_argument > 100:
                arg = 100
                local_logger.info("allowed count in range of 0-100")
            else:
                arg = parsed_argument
        else:
            local_logger.error("inputted not digit argument (string or with minus)")
    return arg

def request_template(endpoint, local_logger):
    response_for_return = None
    try:
        response = requests.get(endpoint).json()
        if response.status_code != 200:
            local_logger.error(f"Request to {endpoint} endpoint finished with {response.status_code} code with \
            {response.reason} reason")
        else:
            response_for_return = response
    except requests.exceptions.ConnectionError:
        local_logger.error("Internet Connection error")
    except requests.exceptions.Timeout:
        local_logger.error("Connection timeout")
    except requests.exceptions.MissingSchema:
        local_logger.error("URL does not exist")
    except:
        local_logger.error("Unknown problem with requesting or DotaAPI")
    finally:
        return response_for_return
