#encoding=utf-8

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
app = Flask('gloryRoadApi')

app.config.from_pyfile('settings.py')
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

db = SQLAlchemy(app)
# print "dir(db):",dir(db)
# print "dir(db.column):",dir(db.column)






























