An example of the application on the data source side.

Using flask, websockets
jinja for templating

websocket doesn't work if downloaded from pip, install from repo

All using python3.7

# Install websockets
go to the websockets and run python3 setup.py install (there is a problem with pipy verison for py3, therefore install manually like this.)

You need Python 3.7 and pip installed.

pip install virtualenv

To create venv in py3:
virtualenv -p python3 venv or just virtualenv venv
.\venv\Scripts\activate
pip install -r requirements.txt


export FLASK_APP=theapp.py

export FLASK_DEBUG=1


# Misc:
Remove from repo but not local:
git rm --cached *.pyc

Dump current packages into a requirements file:
pip freeze > requirements.txt

export FLASK_DEBUG=1