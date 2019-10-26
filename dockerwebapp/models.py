from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from dockerwebapp import db,login_manager,app
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

class User(db.Model,UserMixin):
	id = db.Column(db.Integer,primary_key=True)
	password = db.Column(db.String(60),nullable=False)

		