# faim2009 

from asyncio.windows_events import NULL
import socket
import threading
import Merkle_Hellman as mh
import json

HOST = "localhost" #"192.168.0.101"
PORT = 8000

def serve(my_conn, clients):
    print("client connected")
    data = json.loads(my_conn.recv(8192).decode())
    if isinstance(data, list):
        print(f"registered public key for {data[0]}")
        clients[data[0]] = data[1]
        my_conn.sendall(json.dumps("ok").encode())

    if isinstance(data, int):
        if data in clients:
            print(f"serving public key for {data}")
            my_conn.sendall(json.dumps(clients[data]).encode())
        else:
            print(f"public key not found for {data}")
            my_conn.sendall(json.dumps("NOT_DEFINED").encode())
    print("client disconnected")    

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen()
clients = {}
my_threads = []

try:

    while True:
        conn, addr = s.accept()
        
        new_t = threading.Thread(target=serve,args=(conn, clients))
        new_t.start()
        my_threads.append(new_t)     

except:
    print("the server has been terminated")
   
finally:
    if s:
        s.close()
    for t in my_threads:
        t.join()