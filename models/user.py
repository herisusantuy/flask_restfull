import sqlite3
from db import db


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    full_name = db.Column(db.String(80))
    address = db.Column(db.String(80))
    phone = db.Column(db.String(80))
    email = db.Column(db.String(80))
    password = db.Column(db.String(80))
    is_driver = db.Column(db.String(80))

    def __init__(self,  username, full_name, address, phone, email, password, is_driver):
        self.username = username
        self.full_name = full_name
        self.address = address
        self.phone = phone
        self.email = email
        self.password = password
        self.is_driver = is_driver

    def json(self):
        return {
            'id': self.id,
            'username': self.username,
            'full_name': self.full_name,
            'address': self.address,
            'phone': self.phone,
            'email': self.email,
            'is_driver': self.is_driver
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    # because we use class method we can change the self with initial like cls
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
