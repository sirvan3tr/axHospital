from flask import render_template, session, redirect, url_for, escape, request
from app import app
from web3.auto import w3
from eth_account.messages import defunct_hash_message

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

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
# omnee portal
students = [
    {   # Record for Sirvan Almasi
        'id': '1', # portal ID
        #'omneeID' : '0xa78e5bb6ff6a849e120985d32532e5067f262e19',
        'omneeID' : '0x6751c5563A62675Ffba7D3220f883c719b7B9F49', # users omnee ID
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

# handle the login sessions
def loginSession():
    if 'omneeID' in session:
        # for testing we only have 1 user thus just return that
        loginJSON = {
                'status' : 1,
                'name' : students[0]['user']['first_name'],
                'status-text' : "You're logged in"
            }
    else:
        loginJSON = {
                'status' : 0,
                'name' : '',
                'status-text' : "You're not logged in"
            }

    return loginJSON


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
    loginJSON = loginSession()
    return render_template('index.html', loginJSON = loginJSON)

@app.route('/register', methods=['GET'])
def register():
    loginJSON = loginSession()
    return render_template('register.html', loginJSON = loginJSON)


@app.route('/login/confirm/<msg>/<sig>', methods=['GET'])
def loginConfirm(msg, sig):
    msgHash = defunct_hash_message(text=msg)
    omneeID = w3.eth.account.recoverHash(msgHash, signature=sig)

    student = [student for student in students if student['omneeID'] == omneeID]
    if len(student) == 0:
        return omneeID
    #return jsonify({'student': student[0]})
    session['omneeID'] = omneeID
    htmlTxt = '<a href="/">Home</a>'
    return 'You are now logged in: ' + omneeID + '<br />' + htmlTxt

@app.route('/login', methods=['Get'])
def login():
    loginJSON = loginSession()
    return render_template('login.html', loginJSON = loginJSON)

@app.route('/logout', methods=['Get'])
def logout():
    session.pop('omneeID', None)
    return redirect(url_for('index'))

@app.route('/profile', methods=['Get'])
def myprofile():
    loginJSON = loginSession()
    return render_template('myprofile.html', loginJSON = loginJSON, tasks = tasks)