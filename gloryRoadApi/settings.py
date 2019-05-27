#encoding=utf-8
import os

from gloryRoadApi import app

dev_db = 'mysql://' + 'root:xiaxiaoxu@127.0.0.1:3306/api'

SECRET_KEY = os.getenv('SECRET_KEY', 'secret string')
SQLALCHEMY_TRACK_MODIFICATIONS = False  # 不追踪对象的修改
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', dev_db)



