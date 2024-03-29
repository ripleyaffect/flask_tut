# import statements
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, render_template, abort, flash
from contextlib import closing

# configuration
DATABASE = '/tmp/flaskr.db'
DEVELOPMENT = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

# create the application
app = Flask(__name__)
app.config.from_object(__name__)

def connect_db():
	return sqlite3.connect(app.config['DATABASE'])

def init_db():
	with closing(connect_db()) as db:
		with app.open_resource('schema.sql', mode='r') as f:
			db.cursor().executescript(f.read())
		db.commit()

@app.before_request
def before_request():
	g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
	db = getattr(g, 'db', None)
	if db is not None:
		db.close()

if __name__ == '__main__':
	app.run()
