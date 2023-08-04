from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'

# Function to initialize the database and create the 'todos' collection
def init_db():
    # Replace the connection string below with the one you received from MongoDB Atlas
    client = MongoClient('mongodb+srv://ownerssolar0x:zhBrFLFAj0pLBkHT@cluster0.kpsljyh.mongodb.net/?retryWrites=true&w=majority')
    db = client['todo_db']
    todos_collection = db['todos']
    todos_collection.create_index([('task', 'text')])
    return todos_collection

# Route to display all tasks
@app.route('/')
def index():
    todos_collection = init_db()
    todos = list(todos_collection.find())
    return render_template('todo.html', todos=todos)

# Route to add a new task
@app.route('/add', methods=['POST'])
def add_todo():
    task = request.form['task']
    done = False
    todos_collection = init_db()
    todos_collection.insert_one({'task': task, 'done': done})
    return redirect(url_for('index'))

# Route to mark a task as done
@app.route('/done/<string:todo_id>')
def mark_done(todo_id):
    todos_collection = init_db()
    todos_collection.update_one({'_id': todo_id}, {'$set': {'done': True}})
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

