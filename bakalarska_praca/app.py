import json

from flask import Flask, request, jsonify, Response, render_template
from flask_cors import CORS

from caesar_cipher import CaesarCipher
from monoalphabetic_cipher import MonoalphabeticCipher
from playfair_cipher import PlayfairCipher
from homophonic_cipher import HomophonicCipher
from polyalphabetic_cipher import PolyalphabeticCipher
from TranspositionCipher import TranspositionCipher
from ADFGVXCipher import ADFGVXCipher

app = Flask(__name__)
CORS(app)
# Prednastavený tajný kľúč
TAJNY_KLUC = "laura"

def over_kluc(zadany_kluc, tajny_kluc=TAJNY_KLUC):
    return zadany_kluc == tajny_kluc

def vytvor_cipher(typ_sifry, data):
    typ_sifry = typ_sifry.lower()

    if typ_sifry == "caesar":
        shift = int(data.get("nastavenie", 3))  # predvolený posun 3 ak nie je zadaný
        cipher = CaesarCipher(shift)
    elif typ_sifry == "monoalphabetic":
        mono_key = data.get("nastavenie")
        cipher = MonoalphabeticCipher(mono_key)
    elif typ_sifry == "playfair":
        playfair_key = data.get("nastavenie")
        cipher = PlayfairCipher(playfair_key)
    elif typ_sifry == "homophonic":
        cipher = HomophonicCipher()
    elif typ_sifry == "polyalphabetic":
        poly_key = data.get("nastavenie")
        cipher = PolyalphabeticCipher(poly_key)
    elif typ_sifry == "transposition":
        transposition_key = data.get("nastavenie")
        cipher = TranspositionCipher(transposition_key)
    elif typ_sifry == "adfgvx":
        adfgvx_key = data.get("nastavenie").upper()
        cipher = ADFGVXCipher(adfgvx_key)
    else:
        raise ValueError("Neznámy typ šifry")

    return cipher

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/encrypt", methods=["POST"])
def encrypt():
    data = request.get_json()
    if data is None:
        return jsonify({"error": "No JSON data provided"}), 400

    zadany_kluc = data.get("tajny_kluc")
    typ_sifry = data.get("typ_sifry")
    message = data.get("message")
    nastavenie = data.get("nastavenie")

    print("zadany kluc",zadany_kluc)
    print("typ sifry",typ_sifry)
    print("message",message)
    print("nastavenie",nastavenie)
    if not zadany_kluc or not typ_sifry or not message:
        return jsonify({"error": "Missing one of required fields: tajny_kluc, typ_sifry, message"}), 400

    # Overenie kľúča
    if not over_kluc(zadany_kluc):
        return jsonify({"error": "Nesprávny kľúč! Prístup zamietnutý."}), 403

    try:
        cipher = vytvor_cipher(typ_sifry, data)
        result = cipher.encrypt(message)
        print("result",result)
        response = json.dumps({"result": result}, ensure_ascii=False)
        return Response(response, content_type='application/json; charset=utf-8')
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/decrypt", methods=["POST"])
def decrypt():
    data = request.get_json()
    if data is None:
        return jsonify({"error": "No JSON data provided"}), 400

    zadany_kluc = data.get("tajny_kluc")
    typ_sifry = data.get("typ_sifry")
    message = data.get("message")

    if not zadany_kluc or not typ_sifry or not message:
        return jsonify({"error": "Missing one of required fields: tajny_kluc, typ_sifry, message"}), 400

    # Overenie kľúča
    if not over_kluc(zadany_kluc):
        return jsonify({"error": "Nesprávny kľúč! Prístup zamietnutý."}), 403

    try:
        cipher = vytvor_cipher(typ_sifry, data)
        result = cipher.decrypt(message)
        response = json.dumps({"result": result}, ensure_ascii=False)
        return Response(response, content_type='application/json; charset=utf-8')
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
