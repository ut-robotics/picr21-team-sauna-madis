from websocket import create_connection
from client import Client

ws = create_connection("ws:https//localhost:8080")
cl = Client(ws)
cl.listen(ws)

