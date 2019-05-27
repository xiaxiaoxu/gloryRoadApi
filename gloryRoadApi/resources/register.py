#encoding=utf-8
from flask import abort

from gloryRoadApi import app, db
from gloryRoadApi.models import User
# from gloryRoadApi.commands import forge,initdb
from flask_restful import reqparse
from flask import Flask, request
from flask_restful import Resource, Api
from flask_restful import fields, marshal_with
import re
# md5加密方法
import hashlib
import os
import uuid
from gloryRoadApi.common import util



# Register接口
class Register(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('username', type=str, help='用户名验证错误', location = 'json')
        # location = 'json'表示请求的参数是json格式的
        self.reqparse.add_argument('password', type=str, help='密码验证错误',location = 'json')
        self.reqparse.add_argument('email', type= str, help='邮箱错误',location = 'json')
        self.args = self.reqparse.parse_args()

    # 处理post请求及参数验证
    def post(self):
        try:
            print "self.args.keys():",self.args.keys()
            userName = self.args['username']
            userPassword = self.args['password']
            email = self.args['email']
            neededParams = self.args.keys()
            print "neededParams:", neededParams
            requestParams = request.json.keys()
            print "requestParams:", requestParams

            # 判断参数是否都有传过来，是否多了，是否错了
            if userName and userPassword and email and util.paramsNumResult(neededParams,requestParams):
                userNameResult = util.validateUsername(userName)
                emailResult = util.validateEmail(email)
                passwordResult = util.validatePassword(userPassword)

                #校验各个参数值是否合法
                if userNameResult and emailResult and passwordResult:
                    if not User.query.filter(User.username == userName).all():  # 查询数据库里是否存在该username
                        userNew = User(username=userName, password=userPassword, email=email)
                        db.session.add(userNew)
                        db.session.commit()
                        return {"code": "00", "userid": userNew.id, "message": u"成功"}
                    else:
                        # 数据库里有重名的
                        return {"code": "01", "message": u"参数值不合法，用户名已存在"}
                else:
                    return {"code": "02", "message": u"参数值不合法，不符合约束条件"}
            else:
                return {"code": "03","message": u"参数错误，可能原因：参数少传了、多传了、写错了"}





        except Exception as e:
            print "error of register: %s" % e
            return {"code": "999","message": u"未知错误"}