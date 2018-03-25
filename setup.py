# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
		name='flask_pixiv',
		version='0.1',
		packets=find_packages(),
		author='faker',
		author_email='b09780978@gmail.com',
		license='MIT',
		description='a web server crawl pixiv image and store you like image src in database.',
		url='https://github.com/b09780978/flask-pixiv',
		download_url='https://github.com/b09780978/flask-pixiv',
		install_requires=[
			'Flask',
			'Flask_SQLAlchemy',
			'Flask_Migrate',
			'Flask_Script',
			'flask-restful',
			'flask-login',
			'requests',
			'beautifulsoup4',
		],
		keywords='flask pixiv crawler python',
		entry_points={ 'console_scripts' : ['flask_pixiv=flask_pixiv.app:run'] },
	)