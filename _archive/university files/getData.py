import requests, datetime
import json, binascii
import web3
from web3 import Web3
from eth_account.messages import defunct_hash_message
from hexbytes import HexBytes

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:9545"))

msg = str(datetime.datetime.now())

pk = '0xae6ae8e5ccbfb04590405997ee2d52d2b330726137b875053c36d94e974d162f'
msgHash = defunct_hash_message(text=msg)

signedMsg = w3.eth.account.signHash(msgHash, private_key=pk)
hexSig = binascii.hexlify(signedMsg.signature)
sig = str(hexSig).split("'")[1]

content = {
    "type": "getData",
    "ownerDID": "0xf2beae25b23f0ccdd234410354cb42d08ed54981", # change this
    "myDID": "0xaa8f61728cb614f37a2fdb8b420c3c33134c7f69",
    "msg" : msg, # NOT SECURE, RUN A PROPER MSG IN FUTURE
    "sig": sig
}

request = requests.post("http://127.0.0.1:5001/api/getdata", json=content)
print(request.text)