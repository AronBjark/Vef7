from os import urandom
from flask import Flask, render_template as rend, url_for, request, session, redirect
from pymysql import *

app = Flask(__name__)
app.secret_key = urandom(14)
connection = connect(host='tsuts.tskoli.is', port=3306, user='2208022210', password='mypassword', database='2208022210_...', autocommit=True)

@app.route('/', methods=['GET', 'POST'])
def index():
	with connection.cursor() as cursor:
		cursor.execute("SELECT * FROM user")
		users = cursor.fetchall()
	if 'user' in session:
		user = session['user']
	else: 
		user = {"username":"none", "password":"none", "name":"none"}
	return rend('index.html', user=user)

@app.route('/login', methods=['GET', 'POST'])
def login():
	r = request.form
	error = False
	if 'user' in session: 
		return redirect(url_for('index'))
	with connection.cursor() as cursor:
		cursor.execute("SELECT * FROM user")
		users = cursor.fetchall()
	if request.method == 'POST':
		error = True
		for u in users:
			if r['username'] == u[0]:
				if r['password'] == u[1]:
					session['user'] = {"username":u[0], "password":u[1], "name":u[2]}
					return redirect(url_for('index'))
	return rend('login.html', error=error)

@app.route('/logout')
def logout():
	if 'user' in session:
		session.pop('user')
	return redirect(url_for('index'))
	
@app.route('/newuser', methods=['GET', 'POST'])
def new_user():
	r = request.form
	error = False
	if 'user' in session:
		return redirect(url_for('index'))
	with connection.cursor() as cursor:
		cursor.execute("SELECT * FROM user")
		users = cursor.fetchall()
	if request.method == 'POST':
		for u in users:
			if u[0] == r['username']:
				return rend('new_user.html', error=True)
		with connection.cursor() as cursor:
			cursor.execute(f"""INSERT INTO User (user, pass, nafn) VALUES
    						   ('{request.form['username']}', '{request.form['password']}', '{request.form['name']}');""")
		return redirect(url_for('login'))
	return rend('new_user.html', error=error)

@app.errorhandler(404)
def error404(error):
	return rend('error.html', error_type=404, error=error)
if __name__ == "__main__":
	app.run(debug=True)
