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
    s.connect((HOST, PORT))
    encrypted_data_to_send = Stream_Encryptor.encrypt(b"Hello, en vagyok a kettes", method)
    s.sendall(bytearray(encrypted_data_to_send))
    data = Stream_Encryptor.decrypt(s.recv(4096), method)
    print(bytearray(data).decode())
    

    