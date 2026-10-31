from flask import Flask, render_template, request, redirect, url_for, make_response, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app) # Wajib biar GitHub Pages bisa nembak API ini

PAYLOAD_FILE = "payload.txt"

def get_payload():
    if os.path.exists(PAYLOAD_FILE):
        with open(PAYLOAD_FILE, "r") as f:
            content = f.read().strip()
            return content if content else None
    return None

# Endpoint buat ngecek apakah web udah harus dideface
@app.route("/api/status", methods=["GET"])
def status():
    payload = get_payload()
    if payload:
        return jsonify({"deface": True, "payload": payload})
    return jsonify({"deface": False})

# Endpoint buat nerima JSO dari form kontak
@app.route("/kirim", methods=["POST"])
def kirim():
    pesan = request.form.get("pesan", "").strip()
    
    if pesan:
        with open(PAYLOAD_FILE, "w") as f:
            f.write(pesan)
        
        # Halaman sukses (tanpa pop-up, tanpa auto-refresh)
        html = """
        <!DOCTYPE html>
        <html lang="id">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Status Pengiriman</title>
            <style>
                body {
                    background-color: #f4f7f6; display: flex; justify-content: center; 
                    align-items: center; height: 100vh; margin: 0; font-family: sans-serif;
                    flex-direction: column; text-align: center;
                }
                h1 { color: #d32f2f; font-size: 2rem; margin-bottom: 10px; }
                p { color: #666; font-size: 1rem; }
            </style>
        </head>
        <body>
            <h1>Pesan Anda Terkirim</h1>
        </body>
        </html>
        """
        return make_response(html)
    
    return "Pesan kosong", 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)