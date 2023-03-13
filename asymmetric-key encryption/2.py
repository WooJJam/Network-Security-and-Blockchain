import os
import random
import time
import hashlib

# SECP256K1 타원 곡선 관련 상수 정의
p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
a = 0x0000000000000000000000000000000000000000000000000000000000000000
b = 0x0000000000000000000000000000000000000000000000000000000000000007
Gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
Gy = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8

# Extended Euclidean Algorithm을 이용한 역원 계산 함수
def modinv(a, n):
    t, newt = 0, 1
    r, newr = n, a

    while newr != 0:
        quotient = r // newr
        t, newt = newt, t - quotient * newt
        r, newr = newr, r - quotient * newr

    if r > 1:
        return None
    if t < 0:
        t += n

    return t

# 개인키 생성 함수
def generate_private_key():
    while True:
        # 강화된 randomness 적용
        seed = os.urandom(16) + str(random.random()).encode() + str(time.time()).encode()
        private_key = hashlib.sha256(seed).hexdigest()

        # 생성된 개인키가 SECP256K1 타원 곡선의 p보다 작은지 확인
        if int(private_key, 16) < p:
            return private_key

# 공개키 생성 함수
def generate_public_key(private_key):
    # 개인키를 정수로 변환
    d = int(private_key, 16)

    # Double-and-Add 알고리즘을 이용한 곱셈 연산
    Qx, Qy = Gx, Gy
    for i in range(256):
        if d & (1 << i):
            Qx, Qy = (Qx * 2 + Qy * 2 + Qx + a) % p, (Qx * 3 + Qy + b) % p
        else:
            Qx, Qy = (Qx * 2 + a) % p, (Qy * 2 + a) % p

    # 곱셈의 역원 계산
    inv = modinv(d, p)

    # 직선 방정식을 이용한 더하기 연산
    R = ((Qx * inv ** 2) % p, ((-Qy) * inv ** 3) % p)

    return R

# 개인키와 공개키 출력
private_key = generate_private_key()
public_key = generate_public_key(private_key)

abc = modinv(6,13)
print(abc)
print("Private key:", private_key)
print("Public key: (", hex(public_key[0]), ",", hex(public_key[1]), ")")
