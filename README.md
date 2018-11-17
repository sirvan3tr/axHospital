An example of the application on the data source side.

Using flask, websockets
jinja for templating

websocket doesn't work if downloaded from pip, install from repo

All using python3.7

# Install websockets
go to the websockets and run python3 setup.py install (there is a problem with pipy verison for py3, therefore install manually like this.)

To create venv in py3:
virtualenv -p python3 venv

export FLASK_APP=theapp.py

From repo but not local:
git rm --cached *.pyc