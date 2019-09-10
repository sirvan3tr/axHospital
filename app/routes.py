from flask import render_template, session, redirect, url_for, escape, request
from app import app
import web3, json, uuid

from web3 import Web3
from eth_account.messages import defunct_hash_message
from hub2 import TrustedHub

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

abi = [
    {
        "constant": True,
        "inputs": [
            {
                "name": "",
                "type": "uint256"
            }
        ],
        "name": "keys",
        "outputs": [
            {
                "name": "title",
                "type": "string"
            },
            {
                "name": "key",
                "type": "string"
            },
            {
                "name": "status",
                "type": "bool"
            },
            {
                "name": "comment",
                "type": "string"
            },
            {
                "name": "approver",
                "type": "address"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [
            {
                "name": "_url",
                "type": "string"
            }
        ],
        "name": "changeMsgServer",
        "outputs": [
            {
                "name": "outcome",
                "type": "string"
            }
        ],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "isApproved",
        "outputs": [
            {
                "name": "approved",
                "type": "bool"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "omneeUser",
        "outputs": [
            {
                "name": "entityType",
                "type": "uint256"
            },
            {
                "name": "owner",
                "type": "address"
            },
            {
                "name": "msgServer",
                "type": "string"
            },
            {
                "name": "approved",
                "type": "bool"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "owner",
        "outputs": [
            {
                "name": "",
                "type": "address"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [
            {
                "name": "_title",
                "type": "string"
            },
            {
                "name": "_key",
                "type": "string"
            },
            {
                "name": "_comment",
                "type": "string"
            }
        ],
        "name": "addKey",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [
            {
                "name": "_index",
                "type": "uint256"
            }
        ],
        "name": "getKey",
        "outputs": [
            {
                "name": "title",
                "type": "string"
            },
            {
                "name": "key",
                "type": "string"
            },
            {
                "name": "status",
                "type": "bool"
            },
            {
                "name": "comment",
                "type": "string"
            },
            {
                "name": "approver",
                "type": "address"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [],
        "name": "lenKeys",
        "outputs": [
            {
                "name": "size",
                "type": "uint256"
            }
        ],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "msgServer",
        "outputs": [
            {
                "name": "msgServer",
                "type": "string"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "name": "_senderAddress",
                "type": "address"
            }
        ],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "constructor"
    }
]

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
        #'deeID' : '0xa78e5bb6ff6a849e120985d32532e5067f262e19',
        'deeID' : '0x6751c5563A62675Ffba7D3220f883c719b7B9F49', # users omnee ID
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
            'deeID' : '0x3d63574ba709e1a77f41bffdfa35d81bec767e82',
#0x7370a704d23904025085daa6299071fa679a69d57c6e22445c3e8cd2b193d853
            'status' : 'active',
            'fee' : 'free' # free, thus no need to pay
        }
    }
]



# handle the login sessions
def loginSession():
    if 'deeID' in session:
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



## Feige-Fiat-Shamir Crypto Identification
## The user will attempt to prove ID
## We need to approve whether we trust the ID issuer
@app.route('/register', methods=['GET'])
def register():
    loginJSON = loginSession()
    # register.html will have the relevant JS code to contact
    # the websocket and handle the interaction
    return render_template('register.html', loginJSON = loginJSON)



@app.route('/issueid', methods=['GET'])
def issueid():
    loginJSON = loginSession()
    return render_template('issueid.html', loginJSON = loginJSON)



## Create the ID here and return the values to the user
## Using the fiat-shamir crypto - create the secret keys
@app.route('/issuedid', methods=['POST'])
def issuedid():
    loginJSON = loginSession()

    # These secrets should not be here
    # You should decide where you want to store them yourself in your app

    '''
    ## GENERATING P AND Q TO GET N
    To generate the primes p and q, generate a random number of bit length k/2 where k is the required bit length of the modulus n; set the low bit (this ensures the number is odd) and set the two highest bits (this ensures that the high bit of n is also set); check if prime (use the Rabin-Miller test); if not, increment the number by two and check again until you find a prime. This is p. Repeat for q starting with a random integer of length k−k/2. If p<q, swop p and q (this only matters if you intend using the CRT form of the private key). In the extremely unlikely event that p=q, check your random number generator! Alternatively, instead of incrementing by 2, just generate another random number each time.

    There are stricter rules in ANSI X9.31 to produce strong primes and other restrictions on p and q to minimise the possibility of certain techniques being used against the algorithm. There is much argument about this topic. It is probably better just to use a longer key length.

    '''
    # 256bit prime generated with openssl prime -generate -bits 256
    p = 108737391008438014623164217168477277531061621767300619083219446155602618695149
    q = 104733366844338231505936350942338934720369370196777483091058558077190366687397
    # n is therefore 512 bits
    # Verify in JavaScript quickly: BigInt(p).toString(2).length 

    #p = 56999 # Secret
    #q = 58403 # Secret

    k = 5 # number of keys

    uniqueRand = uuid.uuid4()
    req_data = request.form
    I = [req_data['name'], req_data['surname'],
        req_data['dateofbirth'], req_data['deeidcontractaddress'], str(uniqueRand)]
    trustedHub = TrustedHub(str(I), p, q, k)
    v, s, j, n, I = trustedHub.createID()

    v = list(map(str, v))
    s = list(map(str, s))
    j = list(map(str, j))
    n = str(n)

    idJSON = json.dumps({'V': v, 'S': s, 'J': j, 'n': n, 'Iraw': req_data, 'I': I})
    return render_template('issuedid.html', loginJSON = loginJSON, idJSON = idJSON)




@app.route('/login/confirm/<msg>/<sig>', methods=['GET'])
def loginConfirm(msg, sig):
    msgHash = defunct_hash_message(text=msg)
    deeID = w3.eth.account.recoverHash(msgHash, signature=sig)

    student = [student for student in students if student['deeID'] == deeID]
    if len(student) == 0:
        return deeID
    #return jsonify({'student': student[0]})
    session['deeID'] = deeID
    htmlTxt = '<a href="/">Home</a>'
    return 'You are now logged in: ' + deeID + '<br />' + htmlTxt



@app.route('/login', methods=['Get'])
def login():
    loginJSON = loginSession()
    return render_template('login.html', loginJSON = loginJSON)



@app.route('/logout', methods=['Get'])
def logout():
    session.pop('deeID', None)
    return redirect(url_for('index'))



@app.route('/profile', methods=['Get'])
def myprofile():
    loginJSON = loginSession()
    return render_template('myprofile.html', loginJSON = loginJSON, tasks = tasks)



@app.route('/verify', methods=['Post'])
def verify():
    req_data = request.get_json()

    # address of the identity holder
    #address = Web3.toChecksumAddress("0xf2beae25b23f0ccdd234410354cb42d08ed54981")

    address = Web3.toChecksumAddress(req_data['recDID'])
    # web3.py instance
    w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:9545"))

    # the public key we wish to verify
    # WE NEED msg AND sig
    # NOT SECURE, IN THE FUTURE RUN PROPER MSG PROCESSING
    msgHash = defunct_hash_message(text=req_data['msg'])
    verPubKey = w3.eth.account.recoverHash(msgHash, signature=req_data['sig'])
    #verPubKey = "0x627306090abab3a6e1400e9345bc60c78a8bef57"


    # set pre-funded account as sender
    w3.eth.defaultAccount = w3.eth.accounts[1]
    print(Web3.toChecksumAddress(w3.eth.defaultAccount))

    # get the DID contract
    DIDContract = w3.eth.contract(
        address=address,
        abi=abi,
    )

    # search through the keys
    # get the number of keys stored on the identity contract
    lenK = DIDContract.functions.lenKeys().call()

    keyFound = False
    for i in range(0, lenK):
        key = DIDContract.functions.getKey(i).call()
        print(key[1])
        if str(key[1])==str(verPubKey):
            return "SUCCESS"
    return "FAIL"



## >> Check deeID contract for a given public key
## Ensure a blockchain is running is defined inside the function
## deeIDAddress: Contract address of the user that we wish to verify
## pubKey: The public key we wish to check if exists inside deeID Contract
def verify(deeIDAddress, pubKey):
    # address of the identity holder
    #address = Web3.toChecksumAddress("0xf2beae25b23f0ccdd234410354cb42d08ed54981")
    #address = Web3.toChecksumAddress(req_data['recDID'])

    # web3.py instance
    w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:9545"))

    # the public key we wish to verify
    # WE NEED msg AND sig
    # NOT SECURE, IN THE FUTURE RUN PROPER MSG PROCESSING
    #msgHash = defunct_hash_message(text=req_data['msg'])
    #verPubKey = w3.eth.account.recoverHash(msgHash, signature=req_data['sig'])
    #verPubKey = "0x627306090abab3a6e1400e9345bc60c78a8bef57"


    # set pre-funded account as sender
    w3.eth.defaultAccount = w3.eth.accounts[1]
    print(Web3.toChecksumAddress(w3.eth.defaultAccount))

    # get the DID contract
    DIDContract = w3.eth.contract(
        address=deeIDAddress,
        abi=abi,
    )

    # search through the keys
    # get the number of keys stored on the identity contract
    lenK = DIDContract.functions.lenKeys().call()

    keyFound = False
    for i in range(0, lenK):
        key = DIDContract.functions.getKey(i).call()
        print(key[1])
        if str(key[1])==str(pubKey):
            return True
    return False


@app.route('/admin/viewdata', methods=['GET'])
def viewdata():
    data = 'hello'
    columns = 'no'
    loginJSON = loginSession()
    return render_template("viewdata.html",
      data=data,
      columns=columns,
      loginJSON = loginJSON,
      title='[ADMIN PAGE] Fetching the Data')


## View all of the deeID contracts on the blockchain
@app.route('/deeIDs', methods=['GET'])
def viewIds():
    # set pre-funded account as sender
    w3.eth.defaultAccount = w3.eth.accounts[1]