#!/usr/bin/env python
import asyncio, websockets
import datetime
import random, string

sockets = {}

def uniqueID(size=12, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

async def sendUser(key):
    if sockets[key]:
        await sockets[key].send('Hello world! :)')

async def main(websocket, path):
    uID = uniqueID() # a unique id for connection
    sockets[uID] = websocket
    await websocket.send(uID)

    for key,val in sockets.items():
        print(key, "=>", val)

    try:
        async for message in websocket:
            print(message)
            for key,val in sockets.items():
                print(key, "=>", val)


            await sendUser(message)


        while True:
            now = datetime.datetime.utcnow().isoformat() + 'Z'
            await websocket.send("Hello world")
            print(len(USERS))
            await asyncio.sleep(random.random() * 3)

    finally:
        del sockets[uID]

start_server = websockets.serve(main, '127.0.0.1', 5678)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
