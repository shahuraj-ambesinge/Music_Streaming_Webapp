from main import db
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column('id', db.Integer, primary_key = True, autoincrement = True)
    fullname = db.Column(db.String(50))
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))

class Creator(db.Model):
    __tablename__ = 'creator'
    creator_id = db.Column('creator_id', db.Integer, primary_key = True, autoincrement = True)
    creator_name = db.Column(db.String(50))
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))
    gender = db.Column(db.String(6))

class Admin(db.Model):
    __tablename__ = 'admin'
    admin_id = db.Column('admin_id', db.Integer, primary_key = True, autoincrement = True)
    admin_name = db.Column(db.String(50))
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))
    gender = db.Column(db.String(6))
