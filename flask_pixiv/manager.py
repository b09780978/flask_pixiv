# -*- coding: utf-8 -*-
import hashlib
from flask import Flask
from flask import request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_restful import Api, Resource
from flask_restful import fields, marshal_with
from flask_login import LoginManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pixiv.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

app.secret_key = 'Fake_your_self_flask_pixiv_api'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = "strong"
login_manager.login_view = "login"
login_manager.login_message = "Please LOG IN"
login_manager.login_message_category = "info"

db = SQLAlchemy(app)
migrate = Migrate(app, db)

'''
	Database Model.
'''
def hash_pwd(password):
	if password is None or len(str(password)) == 0:
		return None
	else:
		hpwd = hashlib.md5(password.encode('utf-8'))
		return hpwd.hexdigest()

class User(db.Model):
	__tablename__ = 'User'

	account = db.Column(db.String(64), primary_key=True)
	hashed_password = db.Column(db.String(100))

	def __init__(self, account, password):
		self.account = account
		self.hashed_password = hash_pwd(password)

class PixivImage(db.Model):
	__tablename__ = 'PixivImage'

	id = db.Column(db.String(64), primary_key=True)
	url = db.Column(db.String(100))

	def __init__(self, id, url):
		self.id = str(id)
		self.url = url

'''
	Use flask_script add database migrate command.
	1. python manager.py db init 2. python manager.py db migrate 3. python manager.py upgrade
								|__________loop____---____________|
'''
manager = Manager(app)
manager.add_command('db', MigrateCommand)

api = Api(app)

MyPixivApi_fields = {
	'id' : fields.String,
	'url' : fields.String,
}

class MyPixivApi(Resource):
	
	@marshal_with(MyPixivApi_fields)
	def get(self, image_id=None, page=None):
		if image_id is not None:
			data = PixivImage.query.get_or_404(image_id)
			return data
		elif page is not None:
			page = 1 if page<1 else page
			data = PixivImage.query.all()
			return data[(page-1)*10:page*10]
		else:
			data = PixivImage.query.all()
			return data
		
	@marshal_with(MyPixivApi_fields)
	def post(self):
		json_data = request.get_json() or {}
		if json_data.get('id', None) is None or json_data.get('url', None) is None:
			abort(404)
		data = PixivImage(id=json_data['id'], url=json_data['url'])
		db.session.add(data)
		db.session.commit()
		return data

	@marshal_with(MyPixivApi_fields)
	def put(self):
		json_data = request.get_json()
		if json_data.get('id', None) is None:
			abort(404)
		data = PixivImage.query.get_or_404(json_data['id'])
		if json_data.get('url', None) is not None:
			data.url = json_data['url']
		db.session.commit()
		return data

	@marshal_with(MyPixivApi_fields)
	def delete(self, image_id):
		data = PixivImage.query.get_or_404(image_id)
		db.session.delete(data)
		db.session.commit()
		return data

api.add_resource(MyPixivApi, '/api/pixiv/<string:image_id>', '/api/pixiv/<int:page>', '/api/pixiv/')

if __name__ == '__main__':
	manager.run()