import random
import math
import fractions as _fractions

class Error(Exception):
    """Base class for exceptions in this module."""

class BinaryConversionError(Error):
    """Custom exception for invalid binary conversions."""
    pass

def modinv(a, b):
    """Returns the modular inverse of a mod b.

    Pre: a < b and gcd(a, b) = 1

    Adapted from https://en.wikibooks.org/wiki/Algorithm_Implementation/
    Mathematics/Extended_Euclidean_algorithm#Python
    """
    saved = b
    x, y, u, v = 0, 1, 1, 0
    while a:
        q, r = b // a, b % a
        m, n = x - u*q, y - v*q
        b, a, x, y, u, v = a, r, u, v, m, n
    return x % saved

def superincreasing_subset_sum(c_prime, w):
    original_byte = 0
    for i in reversed(range(len(w))):
        if c_prime >= w[i]:
            original_byte |= 1 << i
            c_prime -= w[i]
    return original_byte

def coprime(a, b):
    """Returns True iff `gcd(a, b) == 1`, i.e. iff `a` and `b` are coprime"""
    return _fractions.gcd(a, b) == 1


def byte_to_bits(byte):
    if not 0 <= byte <= 255:
        raise BinaryConversionError(byte)

    out = []
    for i in range(8):
        out.append(byte & 1)
        byte >>= 1
    return out[::-1]


def bits_to_byte(bits):
    if not all(bit == 0 or bit == 1 for bit in bits):
        raise BinaryConversionError("Invalid bitstring passed")

    byte = 0
    for bit in bits:
        byte *= 2
        if bit:
            byte += 1
    return byte

def generate_keys():
  private_key = generate_private_key()
  public_key = create_public_key(private_key)
  return private_key, public_key

def generate_private_key(n=8):
    """Generate a private key for use in the Merkle-Hellman Knapsack Cryptosystem

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
    w = []
    total = 0
    for i in range(n):
      total += random.randint(total+1, 2*total+1)
      w.append(total)

    q = random.randint(total+1, 2*total+1)

    r = random.randint(2, q)
    while math.gcd(r, q) != 1:
      r = random.randint(2, q)

    return (w, q, r)

def create_public_key(private_key):
    """Creates a public key corresponding to the given private key.

    To accomplish this, you only need to build and return `beta` as described in the handout.

        beta = (b_1, b_2, ..., b_n) where b_i = r × w_i mod q

    Hint: this can be written in one line using a list comprehension

    @param private_key The private key
    @type private_key 3-tuple `(w, q, r)`, with `w` a n-tuple, and q and r ints.

    @return n-tuple public key
    """
    B = [(s * private_key[2]) % private_key[1] for s in private_key[0]]
    return B


def encrypt(message, public_key):
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
    # Separate the message into chunks the size of the public key
    message_chunks = [message[i:i+len(public_key)] for i in range(0, len(message), len(public_key))]

    encrypted_chunks = []
    # For each chunk, encrypt it
    for chunk in message_chunks:
        encrypted_chunk = []
        # Convert each byte to a list of bits
        chunk_bits = [byte_to_bits(byte) for byte in chunk]
        # Zip the chunk bits with the public key
        zipped = zip(chunk_bits, public_key)
        # Encrypt the chunk by summing the products of the bits and the key
        for bits, key in zipped:
            encrypted_chunk.append(sum(bit * key for bit in bits))
        encrypted_chunks.append(encrypted_chunk)

    return encrypted_chunks


def decrypt(message, private_key):
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
    # Extract w, q, and r from the private key
    w, q, r = private_key
    # Compute the modular inverse of r mod q
    s = modinv(r, q)
    message = [item for sublist in message for item in sublist]
    decrypted_chunks = []
    # For each encrypted chunk, decrypt it
    for chunk in message:
        # Compute c' = cs (mod q)
        chunk = int(chunk)
        c_prime = (chunk * s) % q
        # Solve the superincreasing subset sum using c' and w to recover the original byte
        decrypted_chunk = superincreasing_subset_sum(c_prime, w)
        decrypted_chunks.append(decrypted_chunk)

    # Reconsitite the encrypted bytes to get the original message back
    return bytearray(decrypted_chunks)
