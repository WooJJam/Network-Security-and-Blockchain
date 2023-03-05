
def vigenere(plaintext, keywords):
    
    vigenereEnc=""
    keywords = keywords.upper()
    i=0

    for x in range (len(plaintext)):
        vigenereEnc += chr(((ord(plaintext[x]) + ord(keywords[i])) % 26)+ord('A'))
        i+=1

        if(i == len(keywords)):
            i=0

    return vigenereEnc

def autokeyCipher(plaintext, key):
    ciphertext = ""
    ciphertext = chr(ord(plaintext[0]) + key)
    if(ord(ciphertext)>91):
        ciphertext = chr(ord(ciphertext)+key-ord('Z')+64)

    for x in range (1, len(plaintext)):
        ciphertext += chr(((ord(plaintext[x]) + ord(plaintext[x-1])) % 26)+ord('A'))

    return ciphertext

if __name__ == '__main__':
    print("평문입력: ", end="")
    plaintext = input()
    plaintext = plaintext.replace(" ", "").upper()
    print("Vigenere 암호? ", end="")
    keywords = input()
    print("* 암호문: ", vigenere(plaintext, keywords))
    print("* 평문: ", plaintext)
    print("자동 키 암호? ", end="")
    key = int(input())
    print("* 암호문: ", autokeyCipher(plaintext, key))
    print("* 평문: ", plaintext)