from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'

# Function to initialize the database and create the 'todos' table
def init_db():
    conn = sqlite3.connect('todos.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL,
            done BOOLEAN NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Route to display all tasks
@app.route('/')
def index():
    init_db()
    conn = sqlite3.connect('todos.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM todos')
    todos = cursor.fetchall()
    conn.close()
    return render_template('todo.html', todos=todos)

# Route to add a new task
@app.route('/add', methods=['POST'])
def add_todo():
    task = request.form['task']
    done = False
    conn = sqlite3.connect('todos.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO todos (task, done) VALUES (?, ?)', (task, done))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

# Route to mark a task as done
@app.route('/done/<int:todo_id>')
def mark_done(todo_id):
    conn = sqlite3.connect('todos.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE todos SET done = ? WHERE id = ?', (True, todo_id))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
