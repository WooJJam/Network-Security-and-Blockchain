from cryptography.fernet import Fernet
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

def read_plaintext():
    h = open('D:\\개쩌는 VS코드!\\Python\\Network Security and Blockchain\\asymmetric-key encryption\\src\\ex1.txt','r')
    plaintext=""
    while True:
        line = h.readline()
        if not line: 
            break
        plaintext += line
    return plaintext

def msg_encrypt(plaintext):
    key = Fernet.generate_key()
    enc_fernet = Fernet(key)
    enc_msg = enc_fernet.encrypt(plaintext)
    return enc_msg, key

def key_encrypt(key):
    h = open('D:\\개쩌는 VS코드!\\Python\\Network Security and Blockchain\\asymmetric-key encryption\\src\\public_key.pem','r')
    public_key = RSA.importKey(h.read())
    encryptor = PKCS1_OAEP.new(public_key)
    enc_key = encryptor.encrypt(key)
    return enc_key

def key_decrypt(enc_key):
    h = open('D:\\개쩌는 VS코드!\\Python\\Network Security and Blockchain\\asymmetric-key encryption\\src\\private_key.pem','r')
    private_key = RSA.import_key(h.read())
    encryptor = PKCS1_OAEP.new(private_key)
    aes_key = encryptor.decrypt(enc_key)
    h.close()
    return aes_key

def msg_decrypt(enc_msg, aes_key):
    dec_fernet = Fernet(aes_key) 
    msg = dec_fernet.decrypt(enc_msg)
    return msg


if __name__ == '__main__':
    plaintext = read_plaintext()
    enc_msg, key = msg_encrypt(plaintext.encode())
    enc_key = key_encrypt(key)
    aes_key = key_decrypt(enc_key)
    msg = msg_decrypt(enc_msg, aes_key)
    print(msg)




