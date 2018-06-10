FROM python
MAINTAINER b09780978 b09780978@gmail.com
WORKDIR /flask_pixiv
ADD . /flask_pixiv

# Update pip and install flask_pixiv python reqirement packages.
RUN python -m pip install -U pip \
&& pip install --editable .

# Create database(use sqlite3).
RUN cd flask_pixiv \
&& python manager.py db init \
&& python manager.py db migrate \
&& python manager.py db upgrade

EXPOSE 80

CMD cd flask_pixiv && flask_pixiv