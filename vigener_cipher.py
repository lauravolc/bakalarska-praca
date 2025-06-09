from cipher_base import CipherBase


class PolyalphabeticCipher(CipherBase):
    def __init__(self, key):
        self.key = key.upper()  # Kľúč prevedieme na veľké písmená
        self.alphabet = (
            "AÁÄBCČDĎEÉFGHIÍJKLMĽĹMNŇOÓÔPQRŔSŠTŤUÚVWXYÝZŽ .,!?-:0123456789"
        )
        self.alphabet_length = len(self.alphabet)

    def encrypt(self, text):
        return self._apply_cipher(text, encrypt=True)

    def decrypt(self, text):
        return self._apply_cipher(text, encrypt=False)

    def _apply_cipher(self, text, encrypt):
        result = ""
        key_repeated = (self.key * (len(text) // len(self.key) + 1))[:len(text)]

        for char, k in zip(text.upper(), key_repeated):
            if char in self.alphabet:
                char_index = self.alphabet.index(char)
                key_index = self.alphabet.index(k)
                shift = key_index if encrypt else -key_index
                result += self.alphabet[(char_index + shift) % self.alphabet_length]
            else:
                # Ak znak nie je v abecede, pridáme ho bez zmeny
                result += char
        return result

    def process_input(self):
        print("\n--- Polyalphabetic Cipher ---")
        text = input("Zadajte správu na šifrovanie alebo dešifrovanie: ").strip()
        action = input("Zvoľte 'sifrovat' alebo 'desifrovat': ").strip().lower()
        key = input("Zadajte kľúč pre polyalfabetickú šifru: ").strip()

        self.key = key.upper()

        if action == "sifrovat":
            result = self.encrypt(text)
            print(f"\nOriginal: {text}")
            print(f"Encrypted: {result}")
        elif action == "desifrovat":
            result = self.decrypt(text)
            print(f"\nEncrypted: {text}")
            print(f"Decrypted: {result}")
        else:
            print("Neplatná voľba!")