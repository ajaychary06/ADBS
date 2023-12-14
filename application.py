from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'  # Change this to a secret key for production

# Database initialization
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Create student table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS student (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        location TEXT NOT NULL,
        email TEXT NOT NULL,
        courseid INTEGER,
        FOREIGN KEY (courseid) REFERENCES courses(id)
    )
''')

# Create university table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS courses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        university_name TEXT NOT NULL,
        program_name TEXT NOT NULL,
        degrees_offered TEXT NOT NULL
    )
''')

conn.commit()
conn.close()


# Routes
@app.route('/')
def index():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Fetch data from both tables
    cursor.execute('SELECT * FROM student')
    students = cursor.fetchall()

    cursor.execute('SELECT * FROM courses')
    courses = cursor.fetchall()

    conn.close()

    return render_template('index.html', students=students, courses=courses)


@app.route('/add', methods=['POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        location = request.form['location']
        email = request.form['email']
        courseid = request.form['courseid']

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        # Insert data into the student table
        cursor.execute('INSERT INTO student (name, location, email, courseid) VALUES (?, ?, ?, ?)',
                       (name, location, email, courseid))

        conn.commit()
        conn.close()

        return redirect(url_for('index'))


@app.route('/delete/<int:id>')
def delete(id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Delete data from the student table
    cursor.execute('DELETE FROM student WHERE id=?', (id,))

    conn.commit()
    conn.close()

    return redirect(url_for('index'))


@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    if request.method == 'POST':
        name = request.form['name']
        location = request.form['location']
        email = request.form['email']
        courseid = request.form['courseid']

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        # Update data in the student table
        cursor.execute('''
            UPDATE student
            SET name=?, location=?, email=?, courseid=?
            WHERE id=?
        ''', (name, location, email, courseid, id))

        conn.commit()
        conn.close()

        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
