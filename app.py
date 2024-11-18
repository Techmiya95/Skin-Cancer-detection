from flask import Flask, render_template, request, session, redirect, flash, url_for
import psycopg2

app = Flask(__name__)
app.secret_key = "skin"

def connect_to_db():
    return psycopg2.connect(
        user="postgres",
        password="Joel@123",
        host="localhost",
        port=5432,
        database="skin"
    )
conn = connect_to_db()
cursor = conn.cursor()


@app.route("/")
def login():
    return render_template("login.html")

@app.route('/add_users', methods=['POST'])
def add_users():
    name = request.form.get('uname')
    email=request.form.get('uemail')
    password=request.form.get('upassword')

    cursor.execute("""
                INSERT INTO login(name, email, password)
               VALUES(%s,%s,%s)
               """,(name,email,password))
    conn.commit()

    session[('user_id')]= cursor.lastrowid
    session['user_name']=name
    session['user_email']=email

    return render_template("successfull.html")

@app.route('/login_validation', methods=['POST'])
def login_validation():
    email = request.form.get('email')
    password = request.form.get('password')

    cursor.execute("SELECT user_id, name, email FROM login WHERE email = %s AND password = %s", (email, password))
    user = cursor.fetchone()

    if user:
        session['user_id'] = user[0]
        session['user_name'] = user[1]
        session['user_email'] = user[2]
        return redirect('/starter')
    else:
        flash('Invalid email or password', 'danger')
        return redirect('/')

@app.route('/starter')
def starter():
    name = session.get('user_name')
    if name:
        return render_template("new.html", name=name)
    else:
        flash('Please log in first.', 'warning')
        return redirect('/')



@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)