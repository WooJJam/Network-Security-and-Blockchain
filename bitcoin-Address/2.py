import os
import random
import time
import hashlib
import Crypto
from Crypto.Hash import RIPEMD160, SHA256
import base58check

p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
G = (0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8)
q = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
a = 0
b = 7

def get_private_key():
    while (True):
        random_str = os.urandom(256 // 8) + str(random.random()).encode() + str(time.time()).encode()
        random_num = hashlib.sha256(random_str).digest()
        private_key = int.from_bytes(random_num, 'big')
        if private_key < p:
            break
    return private_key


def euclidian(b, n):
    r1 = n
    r2 = b if b > 0 else b+n
    t1 = 0
    t2 = 1
    while r2 > 0:
        q = r1 // r2
        r = r1 - q * r2
        r1 = r2
        r2 = r
        t = t1 - q * t2
        t1 = t2
        t2 = t
    if r1 == 1:
        return t1 if t1 > 0 else t1 + n
    else:
        return None

def euclidean_algorithm(a, b):
    if b == 0:
        return (a, 1, 0)
    else:
        gcd, x, y = euclidean_algorithm(b, a % b)
        return (gcd, y, x - (a // b) * y)

def find_inverse(a, p):
    gcd, x, y = euclidean_algorithm(a, p)
    if gcd == 1:
        return x % p
    else:
        return None

def add(point1: list, point2: list):
    if point1 == point2:
        w = (3 * point1[0] ** 2 + a) * euclidian((2 * point1[1]),p) % p
    else:
        w = (point2[1]- point1[1]) * euclidian( point2[0] - point1[0], p) % p
    if w < 0:
        w += p
    x3 = (w ** 2 - point1[0] - point2[0]) % p
    y3 = (w * (point1[0] - x3) - point1[1]) % p
    if x3 < 0:
        x3 += p
    if y3 < 0:
        y3 += p
    point3 = [x3, y3]
    return point3

def double_and_add(x, G: list):
    binary = bin(x)
    K = G
    for i in range(3, len(binary)):
        if binary[i] == '1':
            K = add(add(K, K), G)
        else:
            K = add(K, K)

    return tuple(K)

def set_corresponding_public_key(e1, ex):
    if(e1[1]%2 == 0):
        public_key ="02"+str(ex[2:])
    else:
        public_key ="03"+str(ex[2:])
    
    return public_key

def sha_hasing(shaText):
    shaText = bytes.fromhex(shaText)
    sha256_hash = hashlib.sha256(shaText).hexdigest()
    return sha256_hash

def ripemd160_hash(ripemdText):
    h = RIPEMD160.new()
    h.update(bytes.fromhex(ripemdText))
    ripemd_hash = h.digest().hex()
    return ripemd_hash
    
def get_address(private_key):
    e1 = double_and_add(private_key, G)
    ex = hex(e1[0])
    
    if(len(ex)!=66):
        while(True):
            if(len(ex) ==66):
                break
            ex += 'f'
            
    public_key = set_corresponding_public_key(e1, ex)
    shaText = sha_hasing(public_key)
    ripemd_hash = ripemd160_hash(shaText)
    public_key_hash = '00' + ripemd_hash
    hash = sha_hasing(public_key_hash)
    hash = sha_hasing(hash)
    checksum = get_checksum(hash)
    public_hash_key = public_key_hash + checksum
    address = base58check_Encoding(public_hash_key)
    return address.decode()

def get_checksum(hash):
    return hash[:8]
    
def base58check_Encoding(base58check_text):
    return base58check.b58encode(bytes.fromhex(base58check_text))


if __name__ == "__main__":
    print("희망하는 주소의 문자열? ", end="")
    text = input()

    while(True):
        private_key = get_private_key()
        address = get_address(private_key)
        index = address.find(text)
        if(index != -1):
            print(f"개인 키 = {hex(private_key)[2:]}")
            print(f"주소 = {address}")
            break
    
        