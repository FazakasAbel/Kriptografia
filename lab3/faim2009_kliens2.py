import socket
import json
import Stream_Encryptor
import Merkle_Hellman
from time import sleep

SERVER_HOST = "localhost"
SERVER_PORT = 8000


def get_public_key(client_id):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_s:
        server_s.connect((SERVER_HOST, SERVER_PORT))
        server_s.sendall(json.dumps(client_id).encode())
        public_key = json.loads(server_s.recv(8192).decode())
    return public_key

def register(client_id, public_key):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_s:
        server_s.connect((SERVER_HOST, SERVER_PORT))
        server_s.sendall(json.dumps((client_id, public_key)).encode())
        status = json.loads(server_s.recv(8192).decode())
    return status == "ok"

def negotiate_seed(private_key, peer_public_key, conn):
    raw_data = conn.recv(8192)
    data = Merkle_Hellman.decrypt(raw_data, private_key)
    print(f"got the following encoded message {data}")
    return json.loads(data.decode())
        
def communicate(my_id, client_id, private_key, peer_public_key):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_s:
        print(SERVER_HOST, SERVER_PORT + my_id)
        client_s.bind((SERVER_HOST, SERVER_PORT + my_id))
        client_s.listen()
        print("my socket is created")
        conn, addr = client_s.accept()
        print(f"{addr} connected")
        seed = negotiate_seed(private_key, peer_public_key, conn)
        print(seed)
        solitaire = Stream_Encryptor.getSolitaire(seed)   
        data = Stream_Encryptor.decrypt(conn.recv(8192), solitaire)
        print(bytearray(data).decode())
        encrypted_data_to_send = Stream_Encryptor.encrypt(b"Hello, en vagyok a kettes", solitaire)
        conn.sendall(bytearray(encrypted_data_to_send))
        
my_id = 2
client_id = 1
private_key, public_key = Merkle_Hellman.generate_keys()
if register(my_id, public_key):
    sleep(5)
    peer_public_key = get_public_key(client_id)
    communicate(my_id, client_id, private_key, peer_public_key)