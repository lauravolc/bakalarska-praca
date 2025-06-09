import sys
import os
import random

from cipher_base import CipherBase

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class HomophonicCipher(CipherBase):
    def __init__(self):
        # Nové unikátne mapovanie
        self.mapping = {
            'a': ['01'], 'á': ['02'], 'ä': ['03'],
            'b': ['04'], 'c': ['05'], 'č': ['06'],
            'd': ['07'], 'ď': ['08'], 'e': ['09'], 'é': ['10'],
            'f': ['11'], 'g': ['12'], 'h': ['13'],
            'i': ['14'], 'í': ['15'], 'j': ['16'], 'k': ['17'],
            'l': ['18'], 'ľ': ['19'], 'ĺ': ['20'],
            'm': ['21'], 'n': ['22'], 'ň': ['23'],
            'o': ['24'], 'ó': ['25'], 'ô': ['26'],
            'p': ['27'], 'q': ['28'], 'r': ['29'], 'ŕ': ['30'],
            's': ['31'], 'š': ['32'], 't': ['33'], 'ť': ['34'],
            'u': ['35'], 'ú': ['36'], 'v': ['37'], 'w': ['38'],
            'x': ['39'], 'y': ['40'], 'ý': ['41'], 'z': ['42'],
            'ž': ['43'], ' ': ['44'], '.': ['45'], ',': ['46'],
            '!': ['47'], '?': ['48'], '-': ['49'],
            '0': ['50'], '1': ['51'], '2': ['52'], '3': ['53'],
            '4': ['54'], '5': ['55'], '6': ['56'], '7': ['57'],
            '8': ['58'], '9': ['59']
        }

        # Reverzné mapovanie pre dešifrovanie
        self.reverse_mapping = {v: k for k, values in self.mapping.items() for v in values}

    def encrypt(self, text):
        result = ""
        for char in text.lower():
            if char in self.mapping:
                code = random.choice(self.mapping[char])
                print(f"Encrypting {char} -> {code}")  # Debugovací výpis
                result += code
            else:
                result += char  # Nezmenené, ak znak nie je v abecede
        return result

    def decrypt(self, text):
        result = ""
        i = 0
        while i < len(text):
            num = text[i:i + 2]  # Vyberieme dvojciferné číslo
            print(f"Processing num: {num}")  # Debugging výpis
            if num in self.reverse_mapping:
                result += self.reverse_mapping[num]
                i += 2
            else:
                print(f"Num not found in reverse_mapping: {num}")  # Debugging výpis
                result += text[i]
                i += 1
        return result

    def check_duplicates(self):
        """Kontrola, či sa kódy neopakujú."""
        seen = set()
        for char, codes in self.mapping.items():
            for code in codes:
                if code in seen:
                    print(f"Duplicate found for code {code} with char {char}")
                seen.add(code)
