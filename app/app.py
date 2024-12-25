from flask import Flask, request, jsonify, Blueprint, render_template, redirect
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS posts (id INTEGER PRIMARY KEY AUTOINCREMENT,content TEXT NOT NULL)''')
    conn.commit()
    conn.close()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        content = request.form["content"]
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO posts (content) VALUES (?)", (content,))
        conn.commit()
        post_id = cursor.lastrowid
        conn.close()
        return redirect(f"/{post_id}")
    return render_template("index.html")

@app.route("/<int:post_id>")
def detail(post_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM posts WHERE id = ?",(post_id,))
    post = cursor.fetchone()
    conn.close()
    if post:
        return render_template("detail.html", post=post)
    else:
        return "Bài viết không tồn tại.", 404

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
