#{"method":"bbs", "p":30000000091, "q":40000000003, "seed":4882516701}
#{"method":"solitaire", "seed":[20, 29, 7, 16, 32, 17, 33, 21, 3, 39, 50, 35, 25, 15, 47, 43, 6, 18, 23, 42, 2, 10, 26, 40, 28, 41, 11, 4, 45, 24, 12, 51, 27, 49, 52, 34, 19, 1, 14, 48, 53, 30, 31, 46, 38, 54, 36, 22, 9, 5, 13, 37, 44, 8]}
import Solitaire
import json

def getSolitaire(seed):
    return Solitaire.Solitaire(seed)
    
def encrypt(bytearray, method):
    key = method.generate_bits(len(bytearray))
    return list(map(lambda tuple: tuple[0] ^ tuple[1], zip(key, bytearray)))

def decrypt(bytearray, method):
    key = method.generate_bits(len(bytearray))
    return list(map(lambda tuple: tuple[0] ^ tuple[1], zip(key, bytearray)))    