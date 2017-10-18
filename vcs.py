### Start by building two programs, one to help you find the period, the other to decipher the message given a period ###

import sys
import argparse
import math
from collections import OrderedDict

#alphabet = '0123456789AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ \t\n\r\x0b\x0c'
alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
known_period_ic = OrderedDict([(.066,1), (.052,2), (.047,3), (.045,4), (.044,5), (.041,10)])
def resolve_known_period_ic(calculated_ic):
    if calculated_ic in known_period_ic:
        period = known_period_ic[calculated_ic]
    else:
        period = [0,0]
        for ic in known_period_ic:
            if calculated_ic < ic:
                period[0] = known_period_ic[ic]
            if calculated_ic > ic:
                period[1] = known_period_ic[ic]
                break
    return period

def encrypt(plain_text, key):
    cipher_text = ''
    for idx in range(len(plain_text)):
        cipher_text += alphabet[(alphabet.index(plain_text[idx])+alphabet.index(key[idx%len(key)])) % len(alphabet)]
    return cipher_text

def decrypt(cipher_text):
    for period in estimate_periods(cipher_text):
        print(period)
    print('you will soon be able to decrypt this:')
    return cipher_text

##### decrpyt helper functions #####

def get_distances(cipher_text):
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
    return substring_table

def get_factors(n): 
    factors = []
    factor = 2
    while not factors and (factor in range(2, int(n)+1)):
        if (n % factor == 0) and not [x for x in range(2, int(math.sqrt(factor))+1) if n % x == 0]:
            factors += [factor] + get_factors(n/factor)
        factor += 1            
    return factors

def get_periods(n):
    periods = [1]
    for x in range(2, int(math.sqrt(n))+1):
        if n % x == 0: periods.extend([x, int(n/x)])
    periods.append(n)
    return periods

def calculate_ic(text):
    if len(text) == 0:
        return 0
    def char_frequencies():
        freq_dict = {}
        for char in text:
            if char in freq_dict:
                freq_dict[char] += 1
            else:
                freq_dict[char] = 1
        return freq_dict
    char_frequency = 0
    for freq in char_frequencies().values():
        char_frequency += freq * (freq - 1)
    return char_frequency / (len(text) * (len(text) - 1))

def estimate_periods(cipher_text):
    period_frequencies = {}
    factor_frequencies = {}
    distances = get_distances(cipher_text)
    for string in sorted(distances, key=len, reverse=True):
        for period in get_periods(distances[string]):
            if period in period_frequencies:
                period_frequencies[period] += 1
            else:
                period_frequencies[period] = 1
        for factor in get_factors(distances[string]):
            if factor in factor_frequencies:
                factor_frequencies[factor] += 1
            else:
                factor_frequencies[factor] = 1
    factor_frequencies = OrderedDict(sorted(factor_frequencies.items(), key=lambda x: x[1], reverse=True))
    period_frequencies = OrderedDict(sorted(period_frequencies.items(), key=lambda x: x[1], reverse=True))
    ic = calculate_ic(cipher_text)
    period_range = resolve_known_period_ic(ic)
    periods = []
    sub_period = 0
    for factor in factor_frequencies:
        if factor == period_range:
            periods.append(factor)
            break
        elif len(period_range) == 2:
            if period_range[1] == 0:
                if factor > 10:
                    periods.append(factor)
            elif factor > period_range[0] and factor < period_range[1]:
                periods.append(factor)
            elif factor < period_range[0]:
                if factor in period_frequencies:
                    if sub_period:
                        temp_period = factor * sub_period
                        if temp_period in period_frequencies:
                            periods.append(temp_period)
                    else:
                        sub_period = factor
    for period in [period for period in period_frequencies if period in periods]:
        yield period

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