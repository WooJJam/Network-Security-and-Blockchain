import hashlib
import time

def sha256(msg):
    return hashlib.sha256(msg).digest()

def bits2target(bits):
    bits = bytes.fromhex(bits)
    exponent = bits[0]
    mantissa = int.from_bytes(bits[1:], byteorder="big")
    target = mantissa * 2**(8*(exponent - 3))
    target = hex(target)[2:].zfill(64)
    return target

def find_nonce(msg, target_bits):
    extra_nonce = int(time.time())
    target = bits2target(target_bits)
    nonce = 0
    while True:
        header = msg + extra_nonce.to_bytes(4, byteorder="little") + nonce.to_bytes(4, byteorder="little")
        hash_result = int.from_bytes(sha256(sha256(header)), byteorder="big")
        if hash_result < int(target,16):
            return nonce, extra_nonce, hash_result
        nonce += 1
        if nonce == 2**32:
            nonce = 0
            extra_nonce += 1

if __name__ == "__main__":
    print("- 메시지의 내용? ",end="")
    msg = input()
    print("- Target bits? ",end="")
    target_bits = input()
    target = bits2target(target_bits)
    start_time = time.time()
    nonce, extra_nonce, hash_result = find_nonce(msg.encode(), target_bits)
    end_time = time.time()
    print(f"- Target: 0x{target}")
    print("- 메시지:", msg, ", Extra nonce:", int(time.time()),", nonce:",nonce)
    print("- 실행 시간:", end_time - start_time, "초")
    print(f"- Hash result: 0x{hex(hash_result).zfill(64)}")
