from flask import Flask, render_template, session, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os

current_dir=os.path.abspath(os.path.dirname(__file__))

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(current_dir, "ganadb.sqlite3")
db = SQLAlchemy()
db.init_app(app) 
app.app_context().push()

app.secret_key = os.urandom(24)


from controller import *


if __name__=='__main__':
    app.run(debug=True)