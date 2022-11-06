#!/usr/bin/env python3 -tt
"""
File: crypto.py
---------------
Assignment 1: Cryptography
Course: CS 41
Name: Fazakas Ábel
SUNet: <SUNet ID>

Replace this with a description of the program.
"""
import string
import numpy as np
import itertools
# Caesar Cipher

def error_handling_caesar(text):
    if len(text) <= 0:
        return False

    for letter in text:
        if letter in string.ascii_lowercase:
            return False

    return True        

def error_handling_vignere(text):
    if len(text) <= 0:
        return False

    for letter in text:
        if letter not in string.ascii_uppercase:
            return False

    return True     

def encrypt_caesar(plaintext):
    """Encrypt plaintext using a Caesar cipher.

    Add more implementation details here.
    """
    if not error_handling_caesar(plaintext):
        raise Exception("Wrong format")
    
    return [string.ascii_uppercase[(ord(char) - ord('A') + 3) % len(string.ascii_uppercase)] if char in string.ascii_letters else char for char in plaintext]

def decrypt_caesar(ciphertext):
    """Decrypt a ciphertext using a Caesar cipher.

    Add more implementation details here.
    """
    if not error_handling_caesar(ciphertext):
        raise Exception("Wrong format")
    
    return [string.ascii_uppercase[(ord(char) - ord('A') + 23) % len(string.ascii_uppercase)] if char in string.ascii_letters else char for char in ciphertext]

# Vigenere Cipher

def encrypt_vigenere(plaintext, keyword):
    """Encrypt plaintext using a Vigenere cipher with a keyword.

    Add more implementation details here.
    """
    if not error_handling_vignere(plaintext):
        raise Exception("Wrong format: plaintext")
    if not error_handling_vignere(plaintext):
        raise Exception("Wrong format: keyword")

    return [string.ascii_uppercase[(ord(char) - 2*ord('A') + ord(keyword[i % len(keyword)])) % len(string.ascii_uppercase)] for (i, char) in enumerate(plaintext)]

def decrypt_vigenere(ciphertext, keyword):
    """Decrypt ciphertext using a Vigenere cipher with a keyword.

    Add more implementation details here.
    """
    if not error_handling_vignere(ciphertext):
        raise Exception("Wrong format: ciphertext")
    if not error_handling_vignere(keyword):
        raise Exception("Wrong format: keyword")

    return [string.ascii_uppercase[(ord(char) - 2*ord('A') + 26 - ord(keyword[i % len(keyword)])) % len(string.ascii_uppercase)] for (i, char) in enumerate(ciphertext)]

# Merkle-Hellman Knapsack Cryptosystem


def encrypt_scytale(plaintext, circumference):
    """Decrypt ciphertext using a Scytale cipher with a keyword.

    Add more implementation details here.
    """
    return "".join(list(itertools.chain.from_iterable([plaintext[i::circumference] for i in range(circumference)])))

def decrypt_scytale(ciphertext, circumference):
    """Decrypt ciphertext using a Scytale cipher with a keyword.

    Add more implementation details here.
    """
    r = (len(ciphertext) // circumference) + 1 
    base = [i * r - max(0, i - len(ciphertext) % circumference) for i in range(circumference)]
    concat = list(itertools.chain.from_iterable([[j + i for j in base] for i in range(r)]))[:len(ciphertext)]
    return   "".join(list(map(lambda i: ciphertext[i], concat)))

def encrypt_binary_scytale(byte_array, circumference):
    """Decrypt ciphertext using a Scytale cipher with a keyword.

    Add more implementation details here.
    """
    return bytearray(list(itertools.chain.from_iterable([byte_array[i::circumference] for i in range(circumference)])))

def decrypt_binary_scytale(byte_array, circumference):
    """Decrypt ciphertext using a Scytale cipher with a keyword.

    Add more implementation details here.
    """
    r = (len(byte_array) // circumference) + 1 
    base = [i * r - max(0, i - len(byte_array) % circumference) for i in range(circumference)]
    concat = list(itertools.chain.from_iterable([[j + i for j in base] for i in range(r)]))[:len(byte_array)]
    return   bytearray(list(map(lambda i: byte_array[i], concat)))

def encrypt_railfence(plaintext, num_rails):
    """Decrypt ciphertext using a Railfence cipher with a keyword.

    Add more implementation details here.
    """
    output = ""
    max_step = 2 * num_rails - 2
    for i in range(num_rails):
        if (i == 0 or
            i == num_rails - 1):
                output += plaintext[i::num_rails + num_rails - 2]
        elif num_rails - i == i + 1:
                output += plaintext[i::num_rails - 1]
        else:
            temp = i
            odd = True
            while temp < len(plaintext):
                output += plaintext[temp]
                temp += ((max_step - (i % num_rails) * 2) if odd else ((i % num_rails) * 2))
                odd = not odd
                
    return output

def decrypt_railfence(ciphertext, num_rails):
    """Decrypt ciphertext using a Railfence cipher with a keyword.

    Add more implementation details here.
    """

    left = [(len(ciphertext) // (2 * (num_rails - 1))) * (2 if i % (num_rails - 1) else 1) for i in range(num_rails)]
 
    for i in range(len(ciphertext) % (2 * (num_rails - 1))):
        if i >= num_rails:
            left[2 * num_rails - i - 2] += 1
        else:
            left[i] += 1
    processed = [0 for i in range(num_rails)]
    index = 0
    output = ciphertext[index]
    row = 0
    #-1 is  down, 1 is up
    direction = 1
    while len(output) < len(ciphertext):
        
        if row == 0 or row == num_rails - 1:
            direction *= -1
        #down
        if direction == -1:
            index += left[row] + processed[row + 1]
        #up
        else:
            index -= processed[row] + left[row - 1]
        
        output += ciphertext[index]  
        processed[row] += 1
        left[row] -= 1
        row -= direction

    return  output

def generate_private_key(n=8):
    """Generate a private key for use in the Merkle-Hellman Knapsack Cryptosystem.

    Following the instructions in the handout, construct the private key components
    of the MH Cryptosystem. This consistutes 3 tasks:

    1. Build a superincreasing sequence `w` of length n
        (Note: you can check if a sequence is superincreasing with `utils.is_superincreasing(seq)`)
    2. Choose some integer `q` greater than the sum of all elements in `w`
    3. Discover an integer `r` between 2 and q that is coprime to `q` (you can use utils.coprime)

    You'll need to use the random module for this function, which has been imported already

    Somehow, you'll have to return all of these values out of this function! Can we do that in Python?!

    @param n bitsize of message to send (default 8)
    @type n int

    @return 3-tuple `(w, q, r)`, with `w` a n-tuple, and q and r ints.
    """
    raise NotImplementedError  # Your implementation here

def create_public_key(private_key):
    """Create a public key corresponding to the given private key.

    To accomplish this, you only need to build and return `beta` as described in the handout.

        beta = (b_1, b_2, ..., b_n) where b_i = r × w_i mod q

    Hint: this can be written in one line using a list comprehension

    @param private_key The private key
    @type private_key 3-tuple `(w, q, r)`, with `w` a n-tuple, and q and r ints.

    @return n-tuple public key
    """
    raise NotImplementedError  # Your implementation here


def encrypt_mh(message, public_key):
    """Encrypt an outgoing message using a public key.

    1. Separate the message into chunks the size of the public key (in our case, fixed at 8)
    2. For each byte, determine the 8 bits (the `a_i`s) using `utils.byte_to_bits`
    3. Encrypt the 8 message bits by computing
         c = sum of a_i * b_i for i = 1 to n
    4. Return a list of the encrypted ciphertexts for each chunk in the message

    Hint: think about using `zip` at some point

    @param message The message to be encrypted
    @type message bytes
    @param public_key The public key of the desired recipient
    @type public_key n-tuple of ints

    @return list of ints representing encrypted bytes
    """
    raise NotImplementedError  # Your implementation here

def decrypt_mh(message, private_key):
    """Decrypt an incoming message using a private key

    1. Extract w, q, and r from the private key
    2. Compute s, the modular inverse of r mod q, using the
        Extended Euclidean algorithm (implemented at `utils.modinv(r, q)`)
    3. For each byte-sized chunk, compute
         c' = cs (mod q)
    4. Solve the superincreasing subset sum using c' and w to recover the original byte
    5. Reconsitite the encrypted bytes to get the original message back

    @param message Encrypted message chunks
    @type message list of ints
    @param private_key The private key of the recipient
    @type private_key 3-tuple of w, q, and r

    @return bytearray or str of decrypted characters
    """
    raise NotImplementedError  # Your implementation here

