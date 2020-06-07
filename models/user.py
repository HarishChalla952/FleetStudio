from db import db

class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))
    role = db.Column(db.String(40))



    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role.upper()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def json(self):
        return {'id': self.id, 'username': self.username, 'role':self.role} 

    @classmethod
    def find_by_userid(cls, user_id):
        a=(cls.query.filter_by(id=user_id).first())
        return (a.json())

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()