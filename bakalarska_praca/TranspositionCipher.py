from cipher_base import CipherBase
import math

class TranspositionCipher(CipherBase):
    def __init__(self, key):
        self.key = key

    def _order_key(self):
        """Vráti indexy stĺpcov v poradí podľa abecedy kľúča."""
        return sorted(range(len(self.key)), key=lambda i: self.key[i])

    def encrypt(self, text):
        """Zašifruje text transpozičnou šifrou."""
        num_columns = len(self.key)
        if num_columns == 0:
            return text

        num_rows = math.ceil(len(text) / num_columns)

        # **DOPLNENIE TEXTU, aby mal správnu dĺžku**
        padded_text = text.ljust(num_rows * num_columns, "_")  # Použijeme "_" namiesto medzery na debug

        # Rozdelenie do mriežky
        grid = [list(padded_text[i * num_columns: (i + 1) * num_columns]) for i in range(num_rows)]

        key_order = self._order_key()

        # **Čítanie po stĺpcoch v správnom poradí**
        encrypted_text = "".join(grid[row][col] for col in key_order for row in range(num_rows))

        return encrypted_text

    def decrypt(self, text):
        """Dešifruje text transpozičnou šifrou."""
        num_columns = len(self.key)
        if num_columns == 0:
            return text

        text_len = len(text)

        if text_len % num_columns != 0:
            raise ValueError(f"Chyba: Dĺžka šifrovaného textu ({text_len}) nie je deliteľná dĺžkou kľúča ({num_columns}).")

        num_rows = text_len // num_columns

        key_order = self._order_key()

        # **Oprava: Rozdelenie na stĺpce správnym spôsobom**
        col_lengths = [num_rows] * num_columns
        extra_chars = text_len % num_columns
        for i in range(extra_chars):
            col_lengths[key_order[i]] += 1

        index = 0
        columns = {}
        for sorted_col_idx, original_col_idx in enumerate(key_order):
            columns[original_col_idx] = text[index: index + col_lengths[sorted_col_idx]]
            index += col_lengths[sorted_col_idx]

        # Debug výpisy na kontrolu
        print(f"Šifrovaný text: {repr(text)}")
        print(f"Počet stĺpcov: {num_columns}, Počet riadkov: {num_rows}")
        print(f"Dĺžky stĺpcov: {col_lengths}")
        print(f"Rozdelené stĺpce: {columns}")

        # **Poskladanie textu po riadkoch v správnom poradí**
        decrypted_text = ""
        for row in range(num_rows):
            for col in range(num_columns):
                if row < len(columns[col]):
                    decrypted_text += columns[col][row]

        return decrypted_text.replace("_", "").rstrip()  # Odstránenie výplňových znakov
