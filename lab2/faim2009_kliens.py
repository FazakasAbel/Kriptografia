import socket
import json
import numpy
import Solitaire
import Blum_Blum_Shub
import Stream_Encryptor

HOST = "localhost"
PORT = 5555

method = Stream_Encryptor.getMethod()
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    
    data = Stream_Encryptor.decrypt(conn.recv(4096), method)
    print(bytearray(data).decode())
    encrypted_data_to_send = Stream_Encryptor.encrypt(b"Hello, en vagyok az egyes", method)
    conn.sendall(bytearray(encrypted_data_to_send))
