from flask import Flask, render_template, request, redirect, jsonify
import psycopg2

app = Flask(__name__)
conn = psycopg2.connect(
    database="forum_db_project",
    user="postgres",
    password="root",
    host="localhost",
    port="5432"
)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        author = request.form['author']
        content = request.form['content']
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO messages (author, content) VALUES (%s, %s)", (author, content))
        conn.commit()
        cur.close()
        return redirect('/')
    else:
        return render_template('index.html', author='')


@app.route('/get_messages', methods=['GET'])
def get_messages():
    cur = conn.cursor()
    cur.execute("SELECT * FROM messages ORDER BY id DESC")
    messages = cur.fetchall()
    return jsonify({'messages': messages})


@app.route('/delete/<int:message_id>', methods=['POST'])
def delete_message(message_id):
    cur = conn.cursor()
    cur.execute("DELETE FROM messages WHERE id = %s", (message_id,))
    conn.commit()
    cur.close()
    return redirect('/')


if __name__ == '__main__':
    '''
    conn.cursor().execute(
        "CREATE TABLE messages (id SERIAL PRIMARY KEY , author TEXT, content TEXT)"
    )
    conn.commit()
    '''
    app.run()
