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

## APIs
Register  
http://127.0.0.1:5000/register                        [POST Request ]  
HEADERS:  
Content-Type : application/json  
BODY :  
{  
	"username": "",  
	"password": "",  
	"role" : ""  
}

Login  
http://127.0.0.1:5000/login                           [POST Request ]  
HEADERS:  
Content-Type : application/json  
BODY:  
{  
	"username": "",  
	"password": ""  
}  


Logout  
http://127.0.0.1:5000/logout                           [POST Request]  
HEADERS:  
Content-Type : application/json  
Authorization : Bearer {{accesscode provided by login }}  
BODY:  
{  
	"username": "",  
	"password": ""     	
}  

Doctor Details  
http://127.0.0.1:5000/doctor			      [POST Request]  
HEADERS:  
Content-Type : application/json  
Authorization : Bearer {{accesscode provided by login }}  
BODY:  
{  
	"specilization": "",  
	"gender": ""  
}  

Medicine Suggestion API                                 [POST Request]  
http://127.0.0.1:5000/medicineSuggestion  
HEADERS:    
Content-Type : application/json    
Authorization : Bearer {{accesscode provided by login }}   
BODY:   
{  
	"doctor_id": ,   
	"gender": "",  
	"symptoms" : ""  
}  

Medicine Respond API                                     [POST Request]  
http://127.0.0.1:5000/medicinesRespond/<string:patient_name>  
HEADERS:  
Content-Type : application/json  
Authorization : Bearer {{accesscode provided by login }}  
BODY:  
{  
	"disease" : "dengue",  
	"prescription" : "Papaya leaf extraction"  
}  

Medicines History API                                     [GET Request]  
http://127.0.0.1:5000/medicinesHistory  
HEADERS:  
Content-Type : application/json  
Authorization : Bearer {{accesscode provided for loggedin user}}  

Patient History API                                       [GET Request]  
http://127.0.0.1:5000/patientHistory  
HEADERS:  
Content-Type : application/json  
Authorization : Bearer {{accesscode provided for loggedin user}}  


Health Suggestion to patient by doctor                    [POST Request]  
http://127.0.0.1:5000/healthSuggestion/<string:patient_name>  
HEADERS:  
Content-Type : application/json  
Authorization : Bearer {{accesscode provided for loggedin user}}  
BODY:  
{  
	"suggestion" : " "  
}  









