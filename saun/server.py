import asyncio
import json
import websockets

async def main(websocket, path):
    print("Starting")
    while True:
        cmd = int(await asyncio.get_event_loop().run_in_executor(None, input, "input:"))

        if cmd == 1:
            name = {
                "signal": "start",
                "targets": ["Io", "SaunaMadis"],
                "baskets": ["blue", "magenta"]
            }
        elif cmd == 2:
            name = {
                "signal": "stop",
                "targets": ["Io", "SaunaMadis"],
            }
        elif cmd == 3:
            name = {
                "signal": "start",
                "targets": ["Io", "SaunaMadis"],
                "baskets": ["magenta", "blue"]
            }
        y = json.dumps(name)
        await websocket.send(y)
        print("Sent")

# Below line has the SERVER IP address, not client.
start_server = websockets.serve(main, 'localhost', 8080)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()