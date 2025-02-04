from cipher_base import CipherBase

class CaesarCipher(CipherBase):
    def __init__(self, shift):
        self.shift = shift
        self.alphabet = "AÁÄBCČDĎEÉFGHIÍJKLMĽĹMNŇOÓÔPQRŔSŠTŤUÚVWXYÝZŽ .,!?-:0123456789aáäbcčdďeéfghiíjklľĺmnňoóôpqrŕsštťuúvwxyýzž"

    def encrypt(self, text):
        print(f"Šifrujem: {text} s posunom {self.shift}")  # Debugging výpis
        return self._apply_cipher(text, self.shift)

    def decrypt(self, text):
        print(f"Dešifrujem: {text} s posunom {-self.shift}")  # Debugging výpis
        return self._apply_cipher(text, -self.shift)

    def _apply_cipher(self, text, shift):
        result = ""
        print(f"Používam posun: {shift}")  # Výpis posunu

        for char in text:
            if char in self.alphabet:
                old_index = self.alphabet.index(char)
                new_index = (old_index + shift) % len(self.alphabet)
                new_char = self.alphabet[new_index]

                # Debugging výstup, ktorý ukáže každú zmenu znaku
                print(f"Znak: {char} ({old_index}) -> {new_char} ({new_index})")

                result += new_char
            else:
                print(f"Znak: {char} nie je v abecede, zostáva nezmenený.")  # Debugging znakov mimo abecedy
                result += char  # Znaky, ktoré nie sú v abecede, zostanú nezmenené

        print(f"Výsledok šifrovania: {result}")  # Finálny výstup
        return result
