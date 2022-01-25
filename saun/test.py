from websocket import create_connection
from client import Client

ws = create_connection("localhost:8888")
cl = Client(ws)
cl.listen(ws)

