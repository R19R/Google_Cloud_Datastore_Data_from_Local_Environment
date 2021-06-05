# import re
# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy.orm import relationship



 
# login = LoginManager()
# db = SQLAlchemy()

# class UserModel(UserMixin, db.Model):
#     __tablename__ = 'users'
    
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(100))
#     filename = db.Column(db.String(100))
#     password_hash = db.Column(db.String())
    
 
#     def set_password(self,password):
#         self.password_hash = generate_password_hash(password)
     
#     def check_password(self,password):
#         return check_password_hash(self.password_hash,password)

#     def get_username(self, username):
#         return self.username


# @login.user_loader
# def load_user(username):
#     return UserModel.query.get(username)


from google.cloud import ndb
from flask_login import UserMixin, LoginManager, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
import os


credentials_path = "F:\Google Cloud\LocalDevelopment.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path

db = ndb.Client()
login = LoginManager()

class User_Details(ndb.Model):
    username = ndb.StringProperty()
    password = ndb.StringProperty()
    filename = ndb.StringProperty()

    @classmethod
    def details_User(det, ancestor_key):
        return det.query(ancestor=ancestor_key).order()


    def set_password(self,password):
        self.password_hash = generate_password_hash(password)
     
    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

    def get_username(self, username):
        return self.username


@login.user_loader
def load_user(user_id):
    return User_Details.query(pk=user_id).get()
