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
    substring_table = {}
    for start_idx in range(len(cipher_text)):
        for end_idx in range(start_idx+2, len(cipher_text)):
            if cipher_text[start_idx:end_idx] in substring_table:
                substring_table[cipher_text[start_idx:end_idx]][0] += 1
                substring_table[cipher_text[start_idx:end_idx]][1].append((start_idx, end_idx))
            else:
                substring_table[cipher_text[start_idx:end_idx]] = [1, [(start_idx, end_idx)]]
    
    # removes all dictionary entries where the substring only occurs once
    single_frequency_keys = [key for key in substring_table if substring_table[key][0] == 1]
    for key in single_frequency_keys: del substring_table[key]
    
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