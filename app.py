from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

# OS-based DB path
if os.name == "nt":   # Windows
    DB_PATH = "database.db"
else:                # Railway / Linux
    DB_PATH = "/tmp/database.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT
        )
    ''')
    conn.commit()
    conn.close()

# ✅ IMPORTANT FIX (RUN DB INIT ALWAYS)
@app.before_request
def setup():
    init_db()

@app.route("/", methods=["GET", "POST"])
def index():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    if request.method == "POST":
        note = request.form["note"]
        cursor.execute("INSERT INTO notes (content) VALUES (?)", (note,))
        conn.commit()

    cursor.execute("SELECT * FROM notes")
    notes = cursor.fetchall()
    conn.close()

    return render_template("index.html", notes=notes)

@app.route("/delete/<int:id>")
def delete(id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM notes WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/")

# Only for local run
if __name__ == "__main__":
    init_db()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)