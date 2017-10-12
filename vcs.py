### Start by building two programs, one to help you find the period, the other to decipher the message given a period ###

import sys
import argparse
from collections import OrderedDict

def encrypt(plain_text, key):
    # alphabet = '0123456789AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ \t\n\r\x0b\x0c'
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    cipher_text = ''
    for idx in range(len(plain_text)):
        cipher_text += alphabet[(alphabet.index(plain_text[idx])+alphabet.index(key[idx%len(key)])) % len(alphabet)]
    return cipher_text

def decrypt(cipher_text):
    period = find_period(cipher_text)
    print('you will soon be able to decrypt this:')
    return cipher_text

def find_period(cipher_text):
    frequency_table = OrderedDict()
    for start in range(len(cipher_text)):
        for end in range(start,len(cipher_text)):
            if cipher_text[start:end] in frequency_table:
                frequency_table[cipher_text[start:end]] += 1
            else:
                frequency_table[cipher_text[start:end]] = 1
    for string, frequency in frequency_table.items():
        if frequency > 1 and len(string) > 1:
            print(string, frequency)

def main(data):
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-d', action='store_true', help="decrypt text")
    group.add_argument('-e', action='store', type=str, help='encrypt text given key E')
    args = parser.parse_args()

    if args.e:
        key = args.e
        plain_text = ''.join(data.readlines()).rstrip()
        cipher_text = encrypt(plain_text, key)
        print(cipher_text)
    elif args.d:
        cipher_text = ''.join(data.readlines()).rstrip()
        plain_text = decrypt(cipher_text)
        print(plain_text)
    else:
        print('usage: vcs.py [-h] [-d | -e E]')

if __name__ == "__main__":
    main(sys.stdin)