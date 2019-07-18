import json
import web3

from web3 import Web3
from eth_account.messages import defunct_hash_message

# web3.py instance
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:9545"))

## Load deeID abi
with open('../build/contracts/deeID.json') as json_file:  
    deeID = json.load(json_file)
    deeIDabi= deeID['abi']


address = Web3.toChecksumAddress(req_data['recDID'])

# get the deeID contract
deeIDContract = w3.eth.contract(
    address=address,
    abi=abi,
)

# address of the identity holder
#address = Web3.toChecksumAddress("0xf2beae25b23f0ccdd234410354cb42d08ed54981")

address = Web3.toChecksumAddress(req_data['recDID'])


# the public key we wish to verify
# WE NEED msg AND sig
# NOT SECURE, IN THE FUTURE RUN PROPER MSG PROCESSING
msgHash = defunct_hash_message(text=req_data['msg'])
verPubKey = w3.eth.account.recoverHash(msgHash, signature=req_data['sig'])
#verPubKey = "0x627306090abab3a6e1400e9345bc60c78a8bef57"


"""
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
"""