### Start by building two programs, one to help you find the period, the other to decipher the message given a period ###

import sys
import argparse
import math
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

##### decrpyt helper functions #####

def find_period(cipher_text):
    substring_table = {}
    for start_idx in range(len(cipher_text)):
        for end_idx in range(start_idx+2, len(cipher_text)):
            if cipher_text[start_idx:end_idx] in substring_table:
                substring_table[cipher_text[start_idx:end_idx]].append(start_idx)
            else:
                substring_table[cipher_text[start_idx:end_idx]] = [start_idx]
    
    invalid_keys = []    
    for string, distances in substring_table.items():
        if len(distances) == 1:
            invalid_keys.append(string)
        else:
            distance = distances[1] - distances[0]
            for idx in range(1, len(distances)-1):
                temp_distance = distances[idx+1] - distances[idx]
                if temp_distance != distance:
                    invalid_keys.append(string)
                    break
            substring_table[string] = distance
    
    # removes all dictionary entries where the substring only occurs once
    for key in invalid_keys: del substring_table[key]
    for string in sorted(substring_table, key=len, reverse=True):
        possible_periods = get_periods(substring_table[string])
        factors = get_factors(substring_table[string])

def get_periods(n):
    periods = [1]
    for x in range(2, int(math.sqrt(n))+1):
        if n % x == 0: periods.extend([x, int(n/x)])
    periods.append(n)
    return periods

def get_factors(n): 
    factors = []
    factor = 2
    while not factors and (factor in range(2, int(n)+1)):
        if (n % factor == 0) and not [x for x in range(2, int(math.sqrt(factor))+1) if n % x == 0]:
            factors += [factor] + get_factors(n/factor)
        factor += 1            
    return factors

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