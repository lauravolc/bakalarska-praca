import random
from cipher_base import CipherBase

class ADFGVXCipher(CipherBase):
    def __init__(self, key):
        self.key = key
        # Pôvodná abeceda, ktorú chcete zachovať
        self.alphabet = "AÁÄBCČDĎEÉFGHIÍJKLMĽĹMNŇOÓÔPQRŔSŠTŤUÚVWXYÝZŽ .,!?-:0123456789"

        # Zvýšená veľkosť tabuľky na 8x8 (64 polí)
        self.grid_size = 8
        # Rozšírené označenie riadkov a stĺpcov na 8 znakov
        self.coordinates_map = "ABCDEFGH"
        self.grid = self.generate_grid()

        # Pre debugging: Vypíše vygenerovanú tabuľku
        print("Vygenerovaná tabuľka (grid):")
        for row in self.grid:
            print(" ".join(row))

    def generate_grid(self):
        """Generuje tabuľku s abecedou a doplní ju o medzery, ak je menej ako 64 znakov."""
        chars = list(self.alphabet)
        random.seed(123)
        random.shuffle(chars)
        # Doplníme do 64 znakov (8x8), ak je ich menej
        while len(chars) < self.grid_size * self.grid_size:
            chars.append(" ")  # zvyšné nevyužité pozície

        # Rozsekáme na riadky po 8 znakov
        grid = [chars[i:i + self.grid_size] for i in range(0, len(chars), self.grid_size)]
        return grid

    def find_coordinates(self, char):
        """Vyhľadá súradnice znaku v tabuľke."""
        for row_idx, row in enumerate(self.grid):
            if char in row:
                return row_idx, row.index(char)
        # Ak znak nie je v tabuľke, vyhodí výnimku
        raise ValueError(f"Znak '{char}' sa nenašiel v tabuľke.")

    def map_coordinates_to_char(self, row, col):
        """Preloží súradnice na znak v tabuľke."""
        try:
            return self.grid[row][col]
        except IndexError:
            raise ValueError(f"Neplatné súradnice ({row}, {col}).")

    def encrypt(self, plaintext):
        """Zašifruje text."""
        plaintext = plaintext.upper()
        intermediate = ""
        for char in plaintext:
            if char in self.alphabet:
                row, col = self.find_coordinates(char)
                intermediate += self.coordinates_map[row] + self.coordinates_map[col]
            else:
                # Znak, ktorý nie je v abecede, sa ignoruje
                print(f"Upozornenie: Znak '{char}' nie je v abecede a bude ignorovaný.")

        if not intermediate:
            raise ValueError("Žiadne platné znaky na šifrovanie.")
        return self.columnar_transposition(intermediate)

    def decrypt(self, ciphertext):
        """Dešifruje text."""
        if len(ciphertext) % 2 != 0:
            raise ValueError("Šifrovaný text má nesprávny počet znakov.")

        # Najskôr zreverzujeme stĺpcovú transpozíciu
        transposed_text = self.columnar_transposition_decrypt(ciphertext)
        print(f"Text po reverznej transpozícii: {transposed_text}")

        plaintext = ""
        for i in range(0, len(transposed_text), 2):
            row = self.coordinates_map.index(transposed_text[i])
            col = self.coordinates_map.index(transposed_text[i + 1])
            plaintext += self.map_coordinates_to_char(row, col)
        return plaintext

    def columnar_transposition(self, text):
        """Vykonáva stĺpcovú transpozíciu."""
        num_columns = len(self.key)
        columns = {i: [] for i in range(num_columns)}
        for i, char in enumerate(text):
            col_index = i % num_columns
            columns[col_index].append(char)

        # Zoradíme stĺpce podľa kľúča
        sorted_keys = sorted((k, i) for i, k in enumerate(self.key))
        encrypted = ""
        for _, index in sorted_keys:
            encrypted += "".join(columns[index])
        return encrypted

    def columnar_transposition_decrypt(self, text):
        """Reverzná stĺpcová transpozícia."""
        num_columns = len(self.key)
        num_rows = len(text) // num_columns
        extra_chars = len(text) % num_columns

        # Zoradíme stĺpce podľa kľúča
        sorted_keys = sorted((k, i) for i, k in enumerate(self.key))
        columns = {i: [] for i in range(num_columns)}

        idx = 0
        for _, col_index in sorted_keys:
            # Dĺžka tohto stĺpca
            length = num_rows + (1 if col_index < extra_chars else 0)
            columns[col_index] = list(text[idx:idx + length])
            idx += length

        # Teraz dáme stĺpce dokopy po riadkoch
        transposed_text = ""
        max_col_len = max(len(c) for c in columns.values())
        for row in range(max_col_len):
            for col in range(num_columns):
                if row < len(columns[col]):
                    transposed_text += columns[col][row]
        return transposed_text
