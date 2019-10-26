from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from dockerwebapp import db,login_manager,app
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

class User(db.Model,UserMixin):
	id = db.Column(db.Integer,primary_key=True)
	username = db.Column(db.String(20),nullable=False)
	password = db.Column(db.String(10),nullable=False)

	def __repr__(self):
		return f"User('{self.username}','{self.password}')"	

		