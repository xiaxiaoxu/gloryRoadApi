#encoding=utf-8
import unittest

from flask import abort

from gloryRoadApi import app, db
from gloryRoadApi.models import User, UserBlog
# from gloryRoadApi.commands import forge,initdb
from flask_restful import reqparse
from flask import Flask, request
from flask_restful import Resource, Api
from flask_restful import reqparse
from flask_restful import request
from flask_restful import fields, marshal_with
from gloryRoadApi.common import util
from gloryRoadApi.resources.login import Login
from gloryRoadApi.resources.register import Register
from gloryRoadApi.resources.create import Create
from gloryRoadApi.resources.update import Update


import time

api = Api(app)



api.add_resource(Register, '/register/', endpoint = 'register')
api.add_resource(Login, '/login/', endpoint = 'login')
api.add_resource(Create, '/create/', endpoint = 'create')
api.add_resource(Update, '/update/', endpoint = 'update')

# 注册shell上下文处理函数
@app.shell_context_processor
def make_shell_context():
    return dict(db = db, User = User, UserBlog = UserBlog)



if __name__ == '__main__':
    #t = Register()

    #print validateUsername('dfgd斯蒂芬f')
    app.run(debug=True)
































