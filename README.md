An example of the application on the data source side.


# Aim
We are concerned with two functions:
1) Identification using the Fiat-Shamir
2) Normal signatures and authentication

Register and Login pages will cater to these two objectives respectively.
You will also require the mobile phone app and the websocket_server


# Install
Using flask, websockets
jinja for templating

websocket doesn't work if downloaded from pip, install from repo

All using python3.7

# Install websockets
go to the websockets and run python3 setup.py install (there is a problem with pipy verison for py3, therefore install manually like this.)

You need Python 3.7 and pip installed.

`pip install virtualenv`

To create venv in py3:
* `virtualenv -p python3 venv`
* or `virtualenv venv`
* `.\venv\Scripts\activate` (Windows)
* `source venv\bin\activate` (Linux/OSX)
* `pip install -r requirements.txt`


* `export FLASK_APP=theapp.py`
* `export FLASK_DEBUG=1`
* `python -m flask run`

# Misc:
Remove from repo but not local:
`git rm --cached *.pyc`

Dump current packages into a requirements file:
pip freeze > requirements.txt

export FLASK_DEBUG=1


------------

python3 -m venv venv
venv\Scripts\activate

export FLASK_APP=plotmaponline.py [on osx]
set FLASK_APP=plotmaponline.py [on windows]

pip freeze > requirements.txt

$env:FLASK_APP = "plotmaponline.py"

deactivate (to get out of venv)

on Windows:
python -m flask run

https://code.visualstudio.com/docs/python/tutorial-flask
