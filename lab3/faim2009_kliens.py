import socket
import json
import Stream_Encryptor
import Merkle_Hellman
from time import sleep

SERVER_HOST = "localhost"
SERVER_PORT = 8000
solitaire_key = [20, 29, 7, 16, 32, 17, 33, 21, 3, 39, 50, 35, 25, 15, 47, 43, 6, 18, 23, 42, 2, 10, 26, 40, 28, 41, 11, 4, 45, 24, 12, 51, 27, 49, 52, 34, 19, 1, 14, 48, 53, 30, 31, 46, 38, 54, 36, 22, 9, 5, 13, 37, 44, 8]

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
    byte_data = json.dumps(solitaire_key).encode()
    print(f"byte form of suggested seed: {byte_data}")
    conn.sendall(json.dumps(Merkle_Hellman.encrypt(byte_data, peer_public_key)).encode())
    print("sent a possible seed to my peer")
    return solitaire_key

def communicate(my_id, client_id, private_key, peer_public_key):
    print(SERVER_HOST, SERVER_PORT + client_id)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_s:
        client_s.connect((SERVER_HOST, SERVER_PORT + client_id))
        print("connected to my peer")
        seed = negotiate_seed(private_key, peer_public_key, client_s)
        print(seed)
        solitaire = Stream_Encryptor.getSolitaire(seed)
        encrypted_data_to_send = Stream_Encryptor.encrypt(b"Hello, en vagyok az egyes", solitaire)
        client_s.sendall(bytearray(encrypted_data_to_send))
        data = Stream_Encryptor.decrypt(client_s.recv(8192), solitaire)
        print(bytearray(data).decode())

my_id = 1
client_id = 2
private_key, public_key = Merkle_Hellman.generate_keys()
if register(my_id, public_key):
    #sleep(5)
    peer_public_key = get_public_key(client_id)
    sleep(7)
    communicate(my_id, client_id, private_key, peer_public_key)