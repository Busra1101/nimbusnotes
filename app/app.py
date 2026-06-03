from flask import Flask, request, redirect
import os
from datetime import datetime, timezone, timedelta

app = Flask(__name__)

DATA_DIR = "/data"
NOTES_FILE = os.path.join(DATA_DIR, "notes.txt")
TURKEY_TIMEZONE = timezone(timedelta(hours=3))


def read_notes():
    os.makedirs(DATA_DIR, exist_ok=True)

    if not os.path.exists(NOTES_FILE):
        return []

    notes = []
    with open(NOTES_FILE, "r", encoding="utf-8") as file:
        for index, line in enumerate(file.readlines()):
            notes.append({"id": index, "text": line.strip()})

    return notes


def save_notes(notes):
    os.makedirs(DATA_DIR, exist_ok=True)

    with open(NOTES_FILE, "w", encoding="utf-8") as file:
        for note in notes:
            file.write(note["text"] + "\n")


@app.route("/")
def index():
    notes = read_notes()

    note_cards = ""
    for note in reversed(notes):
        note_cards += f"""
        <div class="note-card">
            <div class="note-text">{note["text"]}</div>
            <form method="POST" action="/delete/{note["id"]}">
                <button class="delete-button" type="submit">Remove</button>
            </form>
        </div>
        """

    empty_message = """
    <div class="empty-state">
        <div class="empty-icon">☁</div>
        <p>Henüz not yok.</p>
    </div>
    """

    return f"""
    <html>
    <head>
        <title>NimbusNotes</title>
        <style>
            * {{
                box-sizing: border-box;
            }}

            body {{
                min-height: 100vh;
                margin: 0;
                padding: 48px 20px;
                font-family: Arial, sans-serif;
                color: #e5edf7;
                background:
                    radial-gradient(circle at top left, rgba(56, 189, 248, 0.22), transparent 32%),
                    radial-gradient(circle at bottom right, rgba(37, 99, 235, 0.25), transparent 35%),
                    linear-gradient(135deg, #08111f, #0f172a 45%, #111827);
            }}

            .shell {{
                max-width: 820px;
                margin: 0 auto;
            }}

            .hero {{
                margin-bottom: 24px;
            }}

            .badge {{
                display: inline-block;
                padding: 7px 12px;
                border: 1px solid rgba(148, 163, 184, 0.35);
                border-radius: 999px;
                color: #bae6fd;
                background: rgba(15, 23, 42, 0.55);
                font-size: 13px;
                margin-bottom: 14px;
            }}

            h1 {{
                margin: 0;
                font-size: 44px;
                letter-spacing: -1px;
            }}

            .subtitle {{
                max-width: 620px;
                color: #94a3b8;
                line-height: 1.6;
                margin-top: 10px;
            }}

            .panel {{
                background: rgba(15, 23, 42, 0.76);
                border: 1px solid rgba(148, 163, 184, 0.24);
                border-radius: 24px;
                padding: 28px;
                box-shadow: 0 24px 80px rgba(0, 0, 0, 0.35);
                backdrop-filter: blur(14px);
            }}

            textarea {{
                width: 100%;
                min-height: 110px;
                padding: 16px;
                border: 1px solid rgba(148, 163, 184, 0.35);
                border-radius: 16px;
                resize: vertical;
                font-size: 15px;
                outline: none;
                color: #e5edf7;
                background:
                    linear-gradient(rgba(2, 6, 23, 0.72), rgba(2, 6, 23, 0.72)),
                    url('/static/clouds.jpg');
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
            }}

            textarea::placeholder {{
                color: #64748b;
            }}

            textarea:focus {{
                border-color: rgba(56, 189, 248, 0.75);
                box-shadow: 0 0 0 4px rgba(56, 189, 248, 0.12);
            }}

            .add-button {{
                margin-top: 14px;
                padding: 12px 18px;
                border: none;
                border-radius: 12px;
                background: linear-gradient(135deg, #38bdf8, #2563eb);
                color: white;
                cursor: pointer;
                font-weight: bold;
                box-shadow: 0 10px 24px rgba(37, 99, 235, 0.28);
            }}

            .section-title {{
                margin-top: 28px;
                margin-bottom: 8px;
                color: #dbeafe;
            }}

            .note-card {{
                display: flex;
                justify-content: space-between;
                gap: 16px;
                align-items: center;
                margin-top: 12px;
                padding: 15px 16px;
                border-radius: 16px;
                background: rgba(30, 41, 59, 0.72);
                border: 1px solid rgba(148, 163, 184, 0.18);
            }}

            .note-text {{
                color: #e2e8f0;
                line-height: 1.5;
                word-break: break-word;
            }}

            .delete-button {{
                padding: 8px 12px;
                border: 1px solid rgba(148, 163, 184, 0.28);
                border-radius: 10px;
                background: rgba(15, 23, 42, 0.85);
                color: #cbd5e1;
                cursor: pointer;
                font-weight: bold;
            }}

            .delete-button:hover {{
                color: white;
                border-color: rgba(56, 189, 248, 0.55);
            }}

            .empty-state {{
                margin-top: 18px;
                padding: 34px;
                text-align: center;
                border-radius: 18px;
                border: 1px dashed rgba(148, 163, 184, 0.32);
                color: #94a3b8;
                background: rgba(2, 6, 23, 0.22);
            }}

            .empty-icon {{
                font-size: 34px;
                color: #7dd3fc;
                margin-bottom: 6px;
            }}

            .footer {{
                margin-top: 22px;
                text-align: center;
                color: #64748b;
                font-size: 13px;
            }}
        </style>
    </head>
    <body>
        <main class="shell">
            <section class="hero">
                <div class="badge">Live Demo </div>
                <h1>NimbusNotes</h1>
                <p class="subtitle">
                    Notes carried by the cloud, kept beyond the rain.
                </p>
            </section>

            <section class="panel">
                <form method="POST" action="/add">
                    <textarea name="note" placeholder="Leave a thought within the cloud..."></textarea>
                    <br>
                    <button class="add-button" type="submit">Add Note</button>
                </form>

                <h2 class="section-title">Notes</h2>
                {note_cards if note_cards else empty_message}

                <div class="footer">
                    by the Rain Keeper
                </div>
            </section>
        </main>
    </body>
    </html>
    """


@app.route("/add", methods=["POST"])
def add_note():
    os.makedirs(DATA_DIR, exist_ok=True)

    note = request.form.get("note", "").strip()

    if note:
        time = datetime.now(TURKEY_TIMEZONE).strftime("%Y-%m-%d %H:%M:%S")
        with open(NOTES_FILE, "a", encoding="utf-8") as file:
            file.write(f"{time} - {note}\n")

    return redirect("/")


@app.route("/delete/<int:note_id>", methods=["POST"])
def delete_note(note_id):
    notes = read_notes()

    if 0 <= note_id < len(notes):
        notes.pop(note_id)
        save_notes(notes)

    return redirect("/")


@app.route("/health")
def health():
    return {"status": "ok", "app": "NimbusNotes", "version": "v6"}


if __name__ == "__main__":
    os.makedirs(DATA_DIR, exist_ok=True)
    app.run(host="0.0.0.0", port=8080)