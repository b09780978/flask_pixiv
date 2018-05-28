# -*- coding: utf-8 -*-
import configparser
import logging
from flask import render_template, session, url_for, redirect, flash
from flask_login import UserMixin
from flask_login import login_required, current_user, login_user, logout_user
from .manager import *
from . import pixiv

# Debug mode.
DEBUG = False

# Get your pixiv account and password for crawl pixiv page.
CONFIG_FILE = 'config.ini'
config = configparser.ConfigParser()
config.read(CONFIG_FILE)
pixiv_id = config['pixiv_api']['pixiv_id']
password = config['pixiv_api']['password']

# Logger setting.
LOGGER_FILENAME = './falsk_pixiv.log'
LOGGER_FORMAT = '%(asctime)-15s %(levelname)s %(process)d %(filename)s %(lineno)d %(message)s'
LOGGER_DATE_FORMAT = '%a %d %b %Y %H:%M:%S'

# Create and set logger.
app.logger.setLevel(logging.DEBUG)

logger_file_handler = logging.FileHandler(LOGGER_FILENAME)
logger_file_handler.setLevel(logging.WARN)

logger_formatter = logging.Formatter(LOGGER_FORMAT, LOGGER_DATE_FORMAT)

logger_file_handler.setFormatter(logger_formatter)
app.logger.addHandler(logger_file_handler)

class Account(UserMixin):
    pass

def query_user(account):
	user = User.query.get(account)
	if user is None:
		return False
	else:
		return True

@login_manager.user_loader
def user_loader(account):
	if query_user(account):
		user = Account()
		user.id = account
		return user
	return None

'''
	User login page.
'''
@app.route('/login', methods=['GET', 'POST'])
def login():
	user_id = session.get('user_id')

	if request.method == 'GET':
		return render_template('login.html')

	if current_user.is_authenticated and query_user(user_id):
		return redirect(url_for('index'))

	account = request.form['username']
	user = User.query.get(account)
	if user is None:
		return render_template("login.html", error="username or password error")

	hpwd = hash_pwd(request.form['password'])
	if hpwd == user.hashed_password:
		user = Account()
		user.id = account
		login_user(user, remember=True)
		flash('Logged in successfully')
		return redirect(url_for('index'))

	return render_template("login.html", error="username or password error")

@app.route('/register', methods=['GET', 'POST'])
def register():
	if request.method == 'GET':
		return render_template('register.html')
	
	account = request.form['username']
	password = request.form['password']
	user = User(account=account, password=password)
	try:
		db.session.add(user)
		db.session.commit()
	except Exception:
		return	render_template('register.html', error='register fail')
	return redirect(url_for('index'))

@app.route('/user/check', methods=['POST'])
def check_user():
	account = request.json['account']
	user = User.query.get(account)
	if user is None:
		return '200'
	else:
		return '404'

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))

'''
	Rank page.
'''
@app.route('/', methods=['GET'])
@app.route('/index/', methods=['GET'])
@app.route('/index/<int:page>', methods=['GET'])
@login_required
def index(page=1):
	page = 1 if page<1 else page
	pool = None
	pixiv_api = None
	try:
		pixiv_api = pixiv.PixivApi(pixiv_id, password)
		pool = pixiv_api.get_follow(page)	
	except (pixiv.PixivApiException, Exception):
		app.logger.error('Get index fail')
		pool = []
	finally:
		del pixiv_api
	return render_template('index.html', data=pool, page=page)

@app.route('/favorate', methods=['GET'])
@login_required
def favorate():
	return render_template('favorate.html')

@app.route('/male', methods=['GET'])
@app.route('/male/', methods=['GET'])
@app.route('/male/<int:page>', methods=['GET'])
@login_required
def rank_male(page=1):
	page = 1 if page<1 else page
	page = 10 if page>10 else page
	pool = None
	pixiv_api = None
	try:
		pixiv_api = pixiv.PixivApi(pixiv_id, password)
		pool = pixiv_api.get_rank(page, male=True, daily=False, r18=False)	
	except (pixiv.PixivApiException, Exception) :
		app.logger.error('Get male rank fail')
		pool = []
	finally:
		del pixiv_api
	return render_template('male.html', page=page, data=pool)

@app.route('/female', methods=['GET'])
@app.route('/female/', methods=['GET'])
@app.route('/female/<int:page>', methods=['GET'])
@login_required
def rank_female(page=1):
	page = 1 if page<1 else page
	page = 10 if page>10 else page
	pool = None
	pixiv_api = None
	try:
		pixiv_api = pixiv.PixivApi(pixiv_id, password)
		pool = pixiv_api.get_rank(page, male=False, daily=False, r18=False)	
	except (pixiv.PixivApiException, Exception) :
		app.logger.error('Get female rank fail')
		pool = []
	finally:
		del pixiv_api
	return render_template('female.html', page=page, data=pool)

@app.route('/male_r18', methods=['GET'])
@app.route('/male_r18/', methods=['GET'])
@app.route('/male_r18/<int:page>', methods=['GET'])
@login_required
def rank_r18_male(page=1):
	page = 1 if page<1 else page
	page = 10 if page>10 else page
	pool = None
	pixiv_api = None
	try:
		pixiv_api = pixiv.PixivApi(pixiv_id, password)
		pool = pixiv_api.get_rank(page, male=True, daily=False, r18=True)
	except (pixiv.PixivApiException, Exception):
		app.logger.error('Get male_r18 rank fail')
		pool = []
	finally:
		del pixiv_api
	return render_template('r18_male.html', page=page, data=pool)

@app.route('/female_r18', methods=['GET'])
@app.route('/female_r18/', methods=['GET'])
@app.route('/female_r18/<int:page>', methods=['GET'])
@login_required
def rank_r18_female(page=1):
	page = 1 if page<1 else page
	page = 10 if page>10 else page
	pool = None
	pixiv_api = None
	try:
		pixiv_api = pixiv.PixivApi(pixiv_id, password)
		pool = pixiv_api.get_rank(page, male=False, daily=False, r18=True)
	except (pixiv.PixivApiException, Exception):
		app.logger.error('Get female_r18 rank fail')
		pool = []
	finally:
		del pixiv_api
	return render_template('r18_female.html', page=page, data=pool)

@app.route('/daily', methods=['GET'])
@app.route('/daily/', methods=['GET'])
@app.route('/daily/<int:page>', methods=['GET'])
@login_required
def rank_daily(page=1):
	page = 1 if page<1 else page
	page = 10 if page>10 else page
	pool = None
	pixiv_api = None
	try:
		pixiv_api = pixiv.PixivApi(pixiv_id, password)
		pool = pixiv_api.get_rank(page, daily=False, r18=False)
	except (pixiv.PixivApiException, Exception):
		app.logger.error('Get daily rank fail')
		pool = []
	finally:
		del pixiv_api
	return render_template('daily.html', page=page, data=pool)

@app.route('/daily_r18', methods=['GET'])
@app.route('/daily_r18/', methods=['GET'])
@app.route('/daily_r18/<int:page>', methods=['GET'])
@login_required
def rank_r18_daily(page=1):
	page = 1 if page<1 else page
	page = 10 if page>10 else page
	pixiv_api = None
	pool = None
	try:
		pixiv_api = pixiv.PixivApi(pixiv_id, password)
		pool = pixiv_api.get_rank(page, daily=False, r18=True)
	except (pixiv.PixivApiException, Exception):
		app.logger.error('Get daily_r18 rank fail')
		pool = []
	except:
		del pixiv_api
	return render_template('r18_daily.html', page=page, data=pool)

def run():
	app.run(host='0.0.0.0', port=80, debug=DEBUG)

if __name__ == '__main__':
	run()
