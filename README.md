# FleetStudio

## Pre-requisites:
1) Python 3
2) Pip
3) virtualenv
4) virtualenvwrapper
5) postman 

## Configuration:
1) Create a virtual environment 
```sh
mkvirtualenv api_venv
```
2) To activate a virtual environment
```sh
workon api_venv
```
3)Install the requirements
```sh
pip install -r requirements.txt
```
4)create required tables
```sh
python3 createDB.py
```
5)start the server on local host
```
python3 app.py
```








