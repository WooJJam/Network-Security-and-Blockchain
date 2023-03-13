import os
import random
import time
import hashlib

p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
Gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
Gy = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8
a = 0
b = 7

def generate_private_key():
    while True:
        rand_str = os.urandom(32) + str(random.random()).encode() + str(time.time()).encode()
        private_key = int(hashlib.sha256(rand_str).hexdigest(), 16)
        
        if private_key < p:
            return private_key

def extended_euclidian(a, b):
    if b == 0:
        return a, 1, 0
    else:
        gcd, x, y = extended_euclidian(b, a % b)
        q = a//b
        return gcd, y, x - q * y

def double_and_add(key, P):
    Q = None
    for i in bin(key)[2:]:
        Q = add_point(Q, Q)
        if i == '1':
            Q = add_point(Q, P)
    return Q

def add_point(P, Q):
    if P is None:
        return Q
    if P[0] == Q[0]:
        inverse = extended_euclidian(2 * P[1], p)[1]
        lam = ((3 * P[0] **2 + a) * inverse) % p
    else:
        inverse = extended_euclidian(Q[0] - P[0], p)[1]
        lam = ((Q[1] - P[1]) * inverse) % p

    x3 = (lam * lam - P[0] - Q[0]) % p
    y3 = (lam * (P[0] - x3) - P[1]) % p

    return x3 ,  y3
        
if __name__ == '__main__':
    private_key =generate_private_key()
    P = double_and_add(private_key, (Gx, Gy))
    public_key = P[0], P[1]
    print(f"개인키(16진수): {hex(private_key)}")
    print(f"개인키(10진수): {private_key}")
    print(f"공개키(16진수): ({hex(public_key[0])}), ({hex(public_key[1])})")
    print(f"공개키(10진수): ({public_key[0]}), ({public_key[1]})")