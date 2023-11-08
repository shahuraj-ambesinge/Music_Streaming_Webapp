
from flask import Flask, render_template, session, request, redirect
from main import app,db
from model import *

@app.route('/')
@app.route('/home')
def start():
    if 'user_id' in session:
        return render_template('index.html')
    else:
        return redirect('/signin')
    
@app.route('/creator_home')
def creator_start():
    if 'creator_id' in session:
        return render_template('creator_index.html')
    else:
        return redirect('/creator_signin')
    


@app.route('/admin_home')
def admin_start():
    if 'admin_id' in session:
        return render_template('admin_index.html')
    else:
        return redirect('/admin_signin')
    
@app.route('/admin_signin')
def admin_sign_in():
    return render_template('admin_signin.html')

@app.route('/admin_signup')
def admin_sign_up():
    return render_template('admin_signup.html')

@app.route('/admin-login-action', methods=['POST'])
def admin_login_action():
    email = request.form.get('email')
    password = request.form.get('password')
    admins = Admin.query.filter_by(email=email, password=password)
    check = []
    for admin in admins:
        check.append(admin)
    if len(check)>=1:
        session['admin_id'] = check[0].admin_id
        return redirect('/admin_home')
    else:
        return redirect('/admin_signin')
    
    
@app.route('/admin-signup-action', methods=['POST'])
def admin_register():
    try:
        admin_name = request.form.get('admin_name')
        email = request.form.get('email')
        password = request.form.get('password')
        gender = request.form.get('gender')
        update_admin = Admin(admin_name=admin_name, email=email, password=password, gender=gender)
        db.session.add(update_admin)
        db.session.flush()
    except Exception as error:
        return "{}".format(error), "admin is not registered"
    else:
        db.session.commit()
        return redirect('/admin_signin')
    
@app.route('/admin_logout')
def admin_logout():
    session.pop('admin_id')
    return redirect('/admin_signin')










@app.route('/signin')
def sign_in():
    return render_template('signin.html')


@app.route('/signup')
def sign_up():
    return render_template('signup.html')

@app.route('/creator_signin')
def creator_sign_in():
    return render_template('creator_signin.html')


@app.route('/creator_signup')
def creator_sign_up():
    return render_template('creator_signup.html')


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
    
@app.route('/user-creator-login-action', methods = ['POST'])
def user_creator_login_action():
    if 'user_id' in session:
        try:
            gender = request.form.get('gender')
            password = request.form.get('password')
            user_creator = User.query.filter_by(id = session['user_id']).first()
            creator_name = user_creator.fullname
            email = user_creator.email
            update_user_creator = Creator(creator_name=creator_name, email=email, password=password, gender=gender)
            db.session.add(update_user_creator)
            db.session.flush()

        except Exception as error:
            return "{}".format(error), "employee is already registered"
        else:
            db.session.commit()
            session.pop('user_id')
            return redirect('/creator_signin')     
        
    else:
        return redirect('/signin')


@app.route('/user_creator')
def user_creator():
    if 'user_id' in session:
        return render_template('user_creator.html')
    else:
        return redirect('/signin')



    




    
@app.route('/creator-login-action', methods=['POST'])
def creator_login_action():
    email = request.form.get('email')
    password = request.form.get('password')
    creators = Creator.query.filter_by(email=email, password=password)
    check = []
    for creator in creators:
        check.append(creator)
    if len(check)>=1:
        session['creator_id'] = check[0].creator_id
        return redirect('/creator_home')
    else:
        return redirect('/creator_signin')
    

    
@app.route('/creator-signup-action', methods=['POST'])
def creator_register():
    try:
        creator_name = request.form.get('creator_name')
        email = request.form.get('email')
        password = request.form.get('password')
        gender = request.form.get('gender')
        update_creator = Creator(creator_name=creator_name, email=email, password=password, gender=gender)
        db.session.add(update_creator)
        db.session.flush()
    except Exception as error:
        return "{}".format(error), "creator is not registered"
    else:
        db.session.commit()
        return redirect('/creator_signin')


        


@app.route('/logout')
def logout():
    session.pop('user_id')
    return redirect('/signin')

@app.route('/creator_logout')
def creator_logout():
    session.pop('creator_id')
    return redirect('/creator_signin')