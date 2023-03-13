from cryptography.fernet import Fernet
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

def read_plaintext():
    print("평문입력: ", end="")
    plaintext = input()
    return plaintext

def msg_encrypt(plaintext):
    key = Fernet.generate_key()
    enc_fernet = Fernet(key)
    enc_msg = enc_fernet.encrypt(plaintext)
    return enc_msg, key

def key_encrypt(key):
    h = open('D:\\Network Security and Blockchain\\asymmetric-key encryption\\src\\public_key.pem','r')
    public_key = RSA.importKey(h.read())
    encryptor = PKCS1_OAEP.new(public_key)
    enc_key = encryptor.encrypt(key)
    return enc_key

def key_decrypt(enc_key):
    h = open('D:\\Network Security and Blockchain\\asymmetric-key encryption\\src\\private_key.pem','r')
    private_key = RSA.import_key(h.read())
    encryptor = PKCS1_OAEP.new(private_key)
    aes_key = encryptor.decrypt(enc_key)
    h.close()
    return aes_key

def msg_decrypt(enc_msg, aes_key):
    dec_fernet = Fernet(aes_key) 
    dec_msg = dec_fernet.decrypt(enc_msg)
    return dec_msg


if __name__ == '__main__':
    plaintext = read_plaintext()
    enc_msg, key = msg_encrypt(plaintext.encode())
    print(f'암호화된 문자열: {enc_msg}')
    enc_key = key_encrypt(key)
    print(f'암호화된 AES key: {enc_key}')
    aes_key = key_decrypt(enc_key)
    dec_msg = msg_decrypt(enc_msg, aes_key)
    print(f'복호화된 문자열: {dec_msg}')




