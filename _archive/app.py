#!flask/bin/python
from flask import Flask, jsonify, render_template

app = Flask(__name__)

tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]

# Example of a database record
omneePortal = [
    {   # Record for Sirvan Almasi
        'id': '1', # portal ID
        'omneeID' : '0x6751c5563a62675ffba7d3220f883c719b7b9f49', # users omnee ID
#0xb50c18d670e82f3f559142d63773b5f60882d337f7d40e78f87973484740ab0d
        'price' : '10', # 10 GBP
        'user' : {
            'first_name' : 'Sirvan',
            'last_name' : 'Almasi',
            'dob' : '26/01/1992',
            'student_number' : '14921600'
        },
        'degree' : {
            'type' : 'BEng',
            'title' : 'Aerospace Engineering',
            'start_date' : '04/10/2010',
            'end_date' : '16/07/2014',
            'status' : 'graduated',
            'result' : '2:1'
        },
        'permission' : {
            'start_date' : '16/07/2018',
            'end_date' : '30/08/2018',
            'omneeID' : '0x3d63574ba709e1a77f41bffdfa35d81bec767e82',
#0x7370a704d23904025085daa6299071fa679a69d57c6e22445c3e8cd2b193d853
            'status' : 'active',
            'fee' : 'free' # free, thus no need to pay
        }
    }
]

@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    return jsonify({'task': task[0]})

@app.route('/', methods=['GET'])
def index():
    return "Hello World!"

if __name__ == '__main__':
    app.run(debug=True)
