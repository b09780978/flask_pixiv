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
    
Easy install packet
------------

    pip install -r requirements.txt
    
Setup:
------------
    edit:
        put your pixiv account and password in config.ini.
        
        pixiv_id = YOUR_PIXIV_ACCOUNT
        
        password = YOUR_PIXIV_PASSWORD

    setup database command:
        
        python manager.py db init
        
        python manager.py db migrate
        
        python manager.py upgrade
        
    run server command:
    
        python app.py
        
Use virtualenv:
------------
    Usage
    ------------
        # create virtual enviroment.
        python -m venv myenv
        
        # activate virtual enviromnent.
        myenv\Scripts\activate
