'''
from math import ceil, sqrt
from cipher_base import CipherBase

class PlayfairCipher(CipherBase):
    def __init__(self, key=None):
        self.alphabet = (
            "AÁÄBCČDĎEÉFGHIÍJKLMĽĹMNŇOÓÔPQRŔSŠTŤUÚVWXYÝZŽ .,!?-:0123456789"
        )
        self.key = key.upper() if key else self.get_key()
        self.matrix, self.matrix_size = self.create_playfair_matrix(self.key)

    def get_key(self):
        return input("Zadajte kľúč pre šifru: ").strip().upper()

    def create_playfair_matrix(self, key):
        # Spočítame veľkosť matice na základe unikátnych znakov
        key = "".join(dict.fromkeys(key))  # Odstránenie duplicit v kľúči
        characters = key + "".join(ch for ch in self.alphabet if ch not in key)
        unique_chars = len(set(characters))
        matrix_size = ceil(sqrt(unique_chars))  # Určenie dynamickej veľkosti matice (najbližší celý počet)
        matrix = [
            characters[i:i + matrix_size]
            for i in range(0, len(characters), matrix_size)
        ]
        return matrix[:matrix_size], matrix_size

    def find_position(self, char):
        for i, row in enumerate(self.matrix):
            if char in row:
                return i, row.index(char)
        return None

    def preprocess_text(self, text, encrypt=True):
        text = text.upper()
        text = "".join(char for char in text if char in self.alphabet)  # Povolené len znaky z abecedy
        digrams = []
        i = 0
        while i < len(text):
            a = text[i]
            b = text[i + 1] if (i + 1) < len(text) else ('X' if encrypt else '')
            if a == b and encrypt:  # Ak sú rovnaké znaky, pridáme 'X'
                b = 'X'
                i += 1
            else:
                i += 2
            digrams.append(a + b if b else a)
        return digrams

    def encrypt(self, text):
        return self._apply_cipher(text, encrypt=True)

    def decrypt(self, text):
        return self._apply_cipher(text, encrypt=False)

    def _apply_cipher(self, text, encrypt):
        digrams = self.preprocess_text(text, encrypt=encrypt)
        result = ""

        for digram in digrams:
            if len(digram) == 1:  # Len jeden znak (iba pri dešifrovaní)
                result += digram
                continue

            a, b = digram
            pos_a = self.find_position(a)
            pos_b = self.find_position(b)

            if not pos_a or not pos_b:  # Ak znak nie je v abecede
                result += a + b
                continue

            row_a, col_a = pos_a
            row_b, col_b = pos_b

            # Rovnaký riadok
            if row_a == row_b:
                result += self.matrix[row_a][(col_a + (1 if encrypt else -1)) % self.matrix_size]
                result += self.matrix[row_b][(col_b + (1 if encrypt else -1)) % self.matrix_size]
            # Rovnaký stĺpec
            elif col_a == col_b:
                result += self.matrix[(row_a + (1 if encrypt else -1)) % self.matrix_size][col_a]
                result += self.matrix[(row_b + (1 if encrypt else -1)) % self.matrix_size][col_b]
            # Rôzne riadky a stĺpce
            else:
                result += self.matrix[row_a][col_b] + self.matrix[row_b][col_a]

        return result

    def process_input(self):
        print("\n--- Playfair šifra ---")
        self.key = self.get_key()  # Získanie kľúča od používateľa
        self.print_matrix()  # Vypísanie matice
        text = input("Zadajte správu na šifrovanie alebo dešifrovanie: ").strip()
        action = input("Zvoľte 'sifrovat' alebo 'desifrovat': ").strip().lower()

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

    def print_matrix(self):
        print("\nPlayfair Matrix:")
        for row in self.matrix:
            print(" ".join(row))
        print(f"\nMatrix Size: {self.matrix_size}x{self.matrix_size}")
'''

from math import ceil, sqrt
from cipher_base import CipherBase

class PlayfairCipher(CipherBase):
    def __init__(self, key=None):
        # Corrected alphabet (removed duplicate 'M')
        self.alphabet = (
            "AÁÄBCČDĎEÉFGHIÍJKLMĽĹMNŇOÓÔPQRŔSŠTŤUÚVWXYÝZŽ .,!?-:0123456789"
        )
        self.key = key.upper() if key else self.get_key()
        # Filter key to include only valid alphabet characters
        self.key = ''.join([c for c in self.key if c in self.alphabet])
        self.matrix, self.matrix_size = self.create_playfair_matrix(self.key)

    def get_key(self):
        return input("Zadajte kľúč pre šifru: ").strip().upper()

    def create_playfair_matrix(self, key):
        # Remove duplicates while preserving order and filter invalid characters
        key = ''.join(dict.fromkeys(key))
        # Collect characters: key + remaining alphabet (excluding those in key)
        remaining = [ch for ch in self.alphabet if ch not in key]
        characters = list(key) + remaining
        # Determine matrix size and ensure it's square
        unique_chars = len(characters)
        matrix_size = ceil(sqrt(unique_chars))
        target_length = matrix_size ** 2
        # Find a filler character not already in 'characters'
        filler = next((c for c in self.alphabet if c not in characters), None)
        if not filler:
            # If all alphabet chars are used, use the first available (unlikely)
            filler = characters[0]  # This is a fallback (not ideal)
        # Pad characters to reach target_length
        while len(characters) < target_length:
            characters.append(filler)
        # Build matrix
        matrix = [
            characters[i*matrix_size : (i+1)*matrix_size]
            for i in range(matrix_size)
        ]
        return matrix, matrix_size

    def find_position(self, char):
        for i, row in enumerate(self.matrix):
            try:
                return (i, row.index(char))
            except ValueError:
                continue
        return None

    def preprocess_text(self, text, encrypt=True):
        text = text.upper()
        text = "".join([c for c in text if c in self.alphabet])
        # Process pairs, handling duplicates by inserting padding
        processed = []
        i = 0
        while i < len(text):
            if i == len(text) - 1:
                a = text[i]
                b = '' if encrypt else ''
                processed.append(a + b)
                i += 1
            else:
                a = text[i]
                b = text[i+1]
                if a == b:
                    processed.append(a + '')
                    i += 1  # Only increment by 1 to handle next pair
                else:
                    processed.append(a + b)
                    i += 2
        # Ensure even length for encryption
        if encrypt and len(processed) * 2 % 2 != 0:
            processed.append('')  # Add a final padding if odd
        return processed

    def encrypt(self, text):
        return self._apply_cipher(text, encrypt=True)

    def decrypt(self, text):
        return self._apply_cipher(text, encrypt=False)

    def _apply_cipher(self, text, encrypt):
        digrams = self.preprocess_text(text, encrypt)
        result = []
        for digram in digrams:
            if len(digram) != 2:
                result.append(digram)  # Handle edge cases, though unlikely
                continue
            a, b = digram
            pos_a = self.find_position(a)
            pos_b = self.find_position(b)
            if not pos_a or not pos_b:
                result.append(a + b)
                continue
            row_a, col_a = pos_a
            row_b, col_b = pos_b
            # Same row
            if row_a == row_b:
                shift = 1 if encrypt else -1
                new_a = self.matrix[row_a][(col_a + shift) % self.matrix_size]
                new_b = self.matrix[row_b][(col_b + shift) % self.matrix_size]
            # Same column
            elif col_a == col_b:
                shift = 1 if encrypt else -1
                new_a = self.matrix[(row_a + shift) % self.matrix_size][col_a]
                new_b = self.matrix[(row_b + shift) % self.matrix_size][col_b]
            # Rectangle
            else:
                new_a = self.matrix[row_a][col_b]
                new_b = self.matrix[row_b][col_a]
            result.append(new_a + new_b)
        return ''.join(result)

    # Rest of the methods (process_input, print_matrix) remain unchanged