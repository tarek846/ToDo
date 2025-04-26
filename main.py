from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
app.secret_key = 'some_secret_key'

# إنشاء قاعدة البيانات
def init_db():
    with sqlite3.connect('tasks.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT NOT NULL
            )
        ''')

init_db()

# الصفحة الرئيسية
@app.route('/')
def home():
    with sqlite3.connect('tasks.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tasks')
        tasks = cursor.fetchall()
    return render_template('index.html', tasks=tasks)

# إضافة مهمة جديدة
@app.route('/add_task', methods=['GET', 'POST'])
def add_task():
    if request.method == 'POST':
        name = request.form['task_name']
        description = request.form['task_description']

        with sqlite3.connect('tasks.db') as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO tasks (name, description) VALUES (?, ?)', (name, description))

        return redirect(url_for('home'))
    
    return render_template('add_task.html')

# حذف مهمة
@app.route('/delete_task/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    with sqlite3.connect('tasks.db') as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
