# Dota parser
## Description

This app parses users data from free Dota api, it uses Flask for serializing.

There is some restrictions from Dota API, example maximum number of getting
top players by rating is 100 etc.

Run program with Docker, or just with Python.

## Usage
### Virtual environment setup
Run virtual environment installation command
```bash
python -m venv venv
```

Activate venv
``` bash
source venv/bin/activate
```

### With Python 
Run requirements installation command
```bash
pip install -r requirements.txt
```

Run app
```bash
python ./app.py --count integer_number_of_needed_players(default 10)
```

Logs will serialize on localhost:5000/ and will save in src/logs.log file.

Parsed data will serialize in localhost:5000/saved_data and will save in parsed_data.json file.

### With docker
Run `docker build -t your_image_name .`.

Run `docker run -d -p 5000:5000 --name container_name image_name --count integer_number_of_needed_players(default 10)`

Logs will serialize on localhost:5000/ and will save in src/logs.log file.

Parsed data will serialize in localhost:5000/saved_data and will save in parsed_data.json file.
