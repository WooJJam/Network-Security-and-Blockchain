import random

def set_codeBook():
    alp = []
    enc = {}
    dec = {}

    for x in range(97, 122):
        alp.append(chr(x))

    random.shuffle(alp)

    for i in range(len(alp)):
        enc[chr(97+i)] = alp[i]
    
    for j in enc:
        index = enc[j]
        dec[index] = j

    return enc, dec

def encryption(text, enc):
    encText = ""
    for i in text:
        if(i == " "):
            encText += i
        else:
            encText += enc[i]
    return encText

def decryption(text, dec):
    decText = ""
    for i in text:
        if(i == " "):
            decText += i
        else:
            decText += dec[i]
    return decText
            
if __name__ == '__main__':
    enc, dec = set_codeBook()
    print("평문입력: ", end="")
    plaintext = input()
    encText = encryption(plaintext, enc)
    print("암호문: ", encText)
    decText = decryption(encText, dec)
    print("복호문: ", decText)
