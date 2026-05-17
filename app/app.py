from flask import Flask, request, redirect
import os
from datetime import datetime

app = Flask(__name__)

DATA_DIR = "/data"
NOTES_FILE = os.path.join(DATA_DIR, "notes.txt")

@app.route("/")
def index():
    os.makedirs(DATA_DIR, exist_ok=True)

    notes = []
    if os.path.exists(NOTES_FILE):
        with open(NOTES_FILE, "r", encoding="utf-8") as file:
            notes = file.readlines()

    note_items = "".join([f"<li>{note}</li>" for note in reversed(notes)])

    return f"""
    <html>
    <head>
        <title>NimbusNotes</title>
    </head>
    <body style="font-family: Arial; margin: 40px;">
        <h1>NimbusNotes</h1>
        <p>Docker ve Kubernetes üzerinde çalışan basit bulut not uygulaması.</p>

        <form method="POST" action="/add">
            <textarea name="note" rows="4" cols="50" placeholder="Not yaz..."></textarea><br><br>
            <button type="submit">Not Ekle</button>
        </form>

        <h2>Notlar</h2>
        <ul>{note_items}</ul>
    </body>
    </html>
    """

@app.route("/add", methods=["POST"])
def add_note():
    os.makedirs(DATA_DIR, exist_ok=True)

    note = request.form.get("note", "").strip()
    if note:
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(NOTES_FILE, "a", encoding="utf-8") as file:
            file.write(f"{time} - {note}\n")

    return redirect("/")

@app.route("/health")
def health():
    return {"status": "ok", "app": "NimbusNotes"}

if __name__ == "__main__":
    os.makedirs(DATA_DIR, exist_ok=True)
    app.run(host="0.0.0.0", port=8080)