from cipher_base import CipherBase
import random


class MonoalphabeticCipher(CipherBase):
    def __init__(self, key):
        self.key = key.upper()
        # Kompletná slovenská abeceda vrátane interpunkcie a čísel
        self.alphabet = (
            "AÁÄBCČDĎEÉFGHIÍJKLMĽĹMNŇOÓÔPQRŔSŠTŤUÚVWXYÝZŽ .,!?-:0123456789"  # Slovenská abeceda
        )
        self.encrypt_mapping, self.decrypt_mapping = self._create_mappings()

    def _create_mappings(self):
        # Odstránime duplicity z kľúča a zabezpečíme poradie
        key_unique = "".join(dict.fromkeys(self.key))
        substitution_alphabet = key_unique + "".join(
            [ch for ch in self.alphabet if ch not in key_unique]
        )

        # Použijeme seed pre konzistentnosť náhodného poradia
        random.seed(self.key)  # Kľúč určuje náhodné poradie
        substitution_alphabet = list(substitution_alphabet)
        random.shuffle(substitution_alphabet)  # Zabezpečíme náhodné, ale deterministické poradie

        # Skontrolujeme, či substitučná abeceda má správnu dĺžku
        if len(substitution_alphabet) != len(self.alphabet):
            raise ValueError("Substitučná abeceda nie je kompletná. Skontrolujte kľúč a abecedu.")

        # Vytvoríme mapovania pre šifrovanie a dešifrovanie
        encrypt_mapping = {
            self.alphabet[i]: substitution_alphabet[i] for i in range(len(self.alphabet))
        }
        decrypt_mapping = {
            substitution_alphabet[i]: self.alphabet[i] for i in range(len(self.alphabet))
        }

        # Debugging výpisy pre overenie mapovania
        print("Encrypt Mapping for numbers:", {k: encrypt_mapping[k] for k in '0123456789'})
        print("Decrypt Mapping for numbers:", {k: decrypt_mapping[k] for k in '0123456789'})

        return encrypt_mapping, decrypt_mapping

    def encrypt(self, text):
        # Prevod na veľké písmená a šifrovanie textu pomocou mapovania
        text = text.upper()
        encrypted_text = "".join(
            self.encrypt_mapping.get(char, char) for char in text
        )
        return encrypted_text

    def decrypt(self, text):
        # Prevod na veľké písmená a dešifrovanie textu pomocou reverzného mapovania
        text = text.upper()
        decrypted_text = "".join(
            self.decrypt_mapping.get(char, char) for char in text
        )
        return decrypted_text

    def process_text(self, text):
        # Spracuje text a vypíše všetky kroky
        print("\n--- PROCESSING TEXT ---")
        print(f"Original text: {text}")

        # Zašifrovanie
        encrypted = self.encrypt(text)
        print(f"Encrypted text: {encrypted}")

        # Dešifrovanie
        decrypted = self.decrypt(encrypted)
        print(f"Decrypted text: {decrypted}")

        # Návrat hodnoty pre ďalšiu analýzu (ak potrebné)
        return {
            "original": text,
            "encrypted": encrypted,
            "decrypted": decrypted
        }
