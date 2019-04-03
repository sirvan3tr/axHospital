import json
import web3

from web3 import Web3
from eth_account.messages import defunct_hash_message

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

# address of the identity holder
#address = Web3.toChecksumAddress("0xf2beae25b23f0ccdd234410354cb42d08ed54981")

address = Web3.toChecksumAddress(req_data['recDID'])


# the public key we wish to verify
# WE NEED msg AND sig
# NOT SECURE, IN THE FUTURE RUN PROPER MSG PROCESSING
msgHash = defunct_hash_message(text=req_data['msg'])
verPubKey = w3.eth.account.recoverHash(msgHash, signature=req_data['sig'])
#verPubKey = "0x627306090abab3a6e1400e9345bc60c78a8bef57"

# web3.py instance
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:9545"))

# set pre-funded account as sender
w3.eth.defaultAccount = w3.eth.accounts[1]
print(Web3.toChecksumAddress(w3.eth.defaultAccount))

# get the DID contract
DIDContract = w3.eth.contract(
    address=address,
    abi=abi,
)

# search through the keys
def keySearch(DIDContract):
    # get the number of keys stored on the identity contract
    lenK = DIDContract.functions.lenKeys().call()

    keyFound = False
    for i in range(0, lenK):
        key = DIDContract.functions.getKey(i).call()
        print(key[i])
        if verPubKey == key:
            keyFound = True
            break
    return keyFound

# if key search was successful:
if keySearch(DIDContract):
    return "Was successful"
else:
	return "Was not successful"
