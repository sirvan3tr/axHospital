from web3.auto import w3
from eth_account.messages import defunct_hash_message
from hexbytes import HexBytes
import json, binascii, websockets, asyncio


omneeID = '0xa78e5bb6ff6a849e120985d32532e5067f262e19'
# Acting like the mobile phone
host = '6fSOx0hpRu7t'

# Add timestamp and other measures to
# counter replay and other attacks
msg = '6fSOx0hpRu7t' + omneeID

# This private keys public key equivalent is registered with data source
pk = '0xb50c18d670e82f3f559142d63773b5f60882d337f7d40e78f87973484740ab0d'
msgHash = defunct_hash_message(text=msg)

signedMsg = w3.eth.account.signHash(msgHash, private_key=pk)
hexSig = binascii.hexlify(signedMsg.signature)
sig = str(hexSig).split("'")[1]

outMsg = json.dumps({
		'type': 'loginSig',
		'host': host,
		'omneeID': omneeID,
		'msg': msg,
		'signature' : str(sig)
	})

async def main():
    async with websockets.connect(
            'ws://localhost:5678') as websocket:

        await websocket.send(outMsg)

asyncio.get_event_loop().run_until_complete(main())