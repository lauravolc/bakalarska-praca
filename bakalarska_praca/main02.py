from caesar_cipher import CaesarCipher
from monoalphabetic_cipher import MonoalphabeticCipher
from playfair_cipher import PlayfairCipher
from homophonic_cipher import HomophonicCipher
from polyalphabetic_cipher import PolyalphabeticCipher
from TranspositionCipher import TranspositionCipher
from ADFGVXCipher import ADFGVXCipher


def over_kluc(zadany_kluc, tajny_kluc="laura"):
    if zadany_kluc != tajny_kluc:
        print("Nesprávny kľúč! Prístup zamietnutý.")
        return False
    return True


def main():
    zadany_kluc = input("Zadajte tajný kľúč pre prístup: ")
    if not over_kluc(zadany_kluc):
        return

    cipher_type = input(
        "Vyberte typ šifry (caesar/monoalphabetic/playfair/homophonic/polyalphabetic/transposition/adfgvx): "
    ).lower()
    message = input("Zadajte správu na šifrovanie alebo dešifrovanie: ")
    action = input("Zvoľte 'sifrovat' alebo 'desifrovat': ").lower()

    if cipher_type == "caesar":
        shift = int(input("Zadajte posun pre Cezarovu šifru: "))
        cipher = CaesarCipher(shift)
    elif cipher_type == "monoalphabetic":
        mono_key = input("Zadajte kľúč pre monoalfabetickú šifru: ")
        cipher = MonoalphabeticCipher(mono_key)
    elif cipher_type == "playfair":
        playfair_key = input("Zadajte kľúč pre Playfair šifru: ")
        cipher = PlayfairCipher(playfair_key)
    elif cipher_type == "homophonic":
        cipher = HomophonicCipher()
    elif cipher_type == "polyalphabetic":
        poly_key = input("Zadajte kľúč pre polyalphabetickú šifru: ")
        cipher = PolyalphabeticCipher(poly_key)
    elif cipher_type == "transposition":
        transposition_key = input("Zadajte kľúč pre transpozičnú šifru: ")
        cipher = TranspositionCipher(transposition_key)
    elif cipher_type == "adfgvx":
        key = input("Zadajte kľúč pre ADFGVX šifru: ").upper()
        try:
            cipher = ADFGVXCipher(key)
        except ValueError as e:
            print(f"Chyba pri vytváraní šifry: {e}")
            return
    else:
        print("Neznámy typ šifry!")
        return

    try:
        if action == "sifrovat":
            result = cipher.encrypt(message)
        elif action == "desifrovat":
            result = cipher.decrypt(message)
        else:
            print("Neznáma akcia!")
            return
        print(f"Výsledok: {result}")
    except Exception as e:
        print(f"Chyba počas spracovania: {e}")


if __name__ == "__main__":
    main()