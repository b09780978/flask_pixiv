# flask-pixiv
    a web server crawl pixiv image and store you like image src in database.

Requirement packet:
------------

python3

    Flask
    
    Flask_SQLAlchemy
    
    Flask_Migrate
    
    Flask_Script
    
    flask-restful
    
    flask-login
    
    requests
    
    beautifulsoup4
    
pip install by setup.py:
------------

    pip install --editable .
        
Setup:
------------
    move folder:
        cd flask_pixiv
    edit:
        put your pixiv account and password in config.ini.
        
        pixiv_id = YOUR_PIXIV_ACCOUNT
        
        password = YOUR_PIXIV_PASSWORD

    setup database command:
        
        python manager.py db init
        
        python manager.py db migrate
        
        python manager.py upgrade
        
    option:
        Debug mode:
            open app.py and set DEBUG = True
        
    run server command:
        flask_pixiv 
        
Use virtualenv(recommand):
------------
    Usage
    ------------
        # create virtual enviroment.
        python -m venv venv
        
        # activate virtual enviromnent.
        venv\Scripts\activate
        
        # update pip.
        python -m pip install -U pip
