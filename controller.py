
from flask import Flask, render_template, session, request, redirect
from main import app,db
from model import User

@app.route('/')
@app.route('/home')
def start():
    if 'user_id' in session:
        return render_template('index.html')
    else:
        return redirect('/signin')


@app.route('/signin')
def sign_in():
    return render_template('signin.html')


@app.route('/signup')
def sign_up():
    return render_template('signup.html')


@app.route('/login-action', methods=['POST'])
def login_action():
    email = request.form.get('email')
    password = request.form.get('password')
    users = User.query.filter_by(email=email, password=password)
    check = []
    for user in users:
        check.append(user)
    if len(check)>=1:
        session['user_id'] = check[0].id
        return redirect('/')
    else:
        return redirect('/signin')


@app.route('/signup-action', methods=['POST'])
def register():
    try:
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        print(username, email, password)
        update_user = User(fullname=username, email=email, password=password)
        db.session.add(update_user)
        db.session.flush()
    except Exception as error:
        return "{}".format(error), "user is not registered"
    else:
        db.session.commit()
        return redirect('/signin')

        


@app.route('/logout')
def logout():
    session.pop('user_id')
    return redirect('/signin')
