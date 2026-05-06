from flask import Flask, request, redirect

import pymysql

app = Flask(__name__)

DB_HOST = 'employee-directory-db.c3ggmq240d5k.eu-central-1.rds.amazonaws.com'

DB_USER = 'admin'

DB_PASS = 'your-rds-password'

DB_NAME = 'employeedirectory'

def get_db():

    return pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASS, database=DB_NAME)

@app.route('/')

def home():

    conn = get_db()

    cursor = conn.cursor()

    cursor.execute('SELECT * FROM employees')

    employees = cursor.fetchall()

    conn.close()

    rows = ''

    for emp in employees:

        rows += f'''

        <tr>

            <td>{emp[1]}</td>

            <td>{emp[2]}</td>

            <td>{emp[3]}</td>

            <td>{emp[4]}</td>

        </tr>'''

    return f'''

    <!DOCTYPE html>

    <html>

    <head>

        <title>Employee Directory</title>

        <style>

            body {{ font-family: Arial, sans-serif; background: #1a1a2e; color: #eee; padding: 40px; }}

            h1 {{ color: #e94560; }}

            table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}

            th {{ background: #16213e; padding: 12px; text-align: left; color: #e94560; }}

            td {{ padding: 12px; border-bottom: 1px solid #333; }}

            tr:hover {{ background: #16213e; }}

            .btn {{ background: #e94560; color: white; padding: 10px 20px; border: none; cursor: pointer; border-radius: 4px; text-decoration: none; }}

        </style>

    </head>

    <body>

        <h1>Employee Directory</h1>

        <a href="/add" class="btn">Add Employee</a>

        <table>

            <tr><th>Name</th><th>Department</th><th>Role</th><th>Email</th></tr>

            {rows}

        </table>

    </body>

    </html>'''

@app.route('/add', methods=['GET', 'POST'])

def add():

    if request.method == 'POST':

        name = request.form['name']

        department = request.form['department']

        role = request.form['role']

        email = request.form['email']

        conn = get_db()

        cursor = conn.cursor()

        cursor.execute('INSERT INTO employees (name, department, role, email) VALUES (%s, %s, %s, %s)', (name, department, role, email))

        conn.commit()

        conn.close()

        return redirect('/')

    return '''

    <!DOCTYPE html>

    <html>

    <head>

        <title>Add Employee</title>

        <style>

            body { font-family: Arial, sans-serif; background: #1a1a2e; color: #eee; padding: 40px; }

            h1 { color: #e94560; }

            input { width: 100%; padding: 10px; margin: 8px 0; background: #16213e; border: 1px solid #333; color: #eee; border-radius: 4px; }

            .btn { background: #e94560; color: white; padding: 10px 20px; border: none; cursor: pointer; border-radius: 4px; }

        </style>

    </head>

    <body>

        <h1>Add Employee</h1>

        <form method="POST">

            <input name="name" placeholder="Name" required/>

            <input name="department" placeholder="Department" required/>

            <input name="role" placeholder="Role" required/>

            <input name="email" placeholder="Email" required/>

            <br/><br/>

            <button type="submit" class="btn">Add Employee</button>

        </form>

    </body>

    </html>'''

if __name__ == '__main__':

    app.run(host='0.0.0.0', port=80)