from cryptography.fernet import Fernet

def encrypt(temp):
    key = Fernet.generate_key()
    fernet = Fernet(key)
    enctext = fernet.encrypt(temp.encode())
    return enctext, fernet

def decrypt(fernet, line):
    return fernet.decrypt(line) 

if __name__ == '__main__':

    f = open('D:\\Network Security and Blockchain\\data.txt', 'r')

    line = ""
    temp = ""
    while True:
        line = f.readline()
        if not line: 
            break
        temp += line

    f.close()
    enctext, fernet = encrypt(temp)

    f = open('D:\\Network Security and Blockchain\\encrypted.txt','w')
    f.write(enctext.decode())
    f.close()

    f = open('D:\\Network Security and Blockchain\\encrypted.txt', 'r')
    line = f.readline()
    dectext = decrypt(fernet, line)
    f.close()

    print(dectext)



