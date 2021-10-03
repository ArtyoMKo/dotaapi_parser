# dota_parser
## Description

This app parsed users data from free Dota api, it uses Flask for serializing.

There is some restrictions from Dota API, example maximum number of getting
top players by rating is 100.

## Usage

### With Python 
Run `pip install -r requirements.txt`, after that run `python ./app.py --count integer_number_of_needed_players_count"`.

Logs will serialize on localhost:5000/ and will save in src/logs.log file.

Parsed data will serialize in localhost:5000/saved_data and will save in parsed_data.json file.

### With docker
Run `docker build -t "your_image_name" .`.

Run `docker run -d -p 5000:5000 --name container_name image_name`

Logs will serialize on localhost:5000/ and will save in src/logs.log file.

Parsed data will serialize in localhost:5000/saved_data and will save in parsed_data.json file.
