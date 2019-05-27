#encoding=utf-8
from gloryRoadApi import app, db
from gloryRoadApi.models import User
# from gloryRoadApi.commands import forge,initdb
from flask_restful import reqparse
from flask import Flask, request
from flask_restful import Resource, Api
import time
from gloryRoadApi.common import util
from flask_restful import fields, marshal_with
import re
# md5加密方法
import hashlib
import os
import uuid
from gloryRoadApi.common import util



# login接口
class Login(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('username', type=str, help='用户名验证错误', location = 'json')
        # location = 'json'表示请求的参数是json格式的
        self.reqparse.add_argument('password', type=str, help='密码验证错误',location = 'json')
        self.args = self.reqparse.parse_args()

    # login接口处理post请求和参数验证
    def post(self):
        try:
            print "Login -> args.keys():",self.args.keys()
            userName = self.args['username']
            userPassword = self.args['password']
            neededParams = self.args.keys()  # 记录self.reqparse.add_argument中添加的参数列表
            print "neededParams:", neededParams
            requestParams = request.json.keys()  # 记录发送请求中携带的参数列表
            print "requestParams:", requestParams

            # 判断参数是否都有传过来，都传过来了，并且没有多传或少传，继续做参数值的校验，否则返回“参数错误”
            if userName and userPassword  and util.paramsNumResult(neededParams, requestParams):
                #到表里查询，是否存在这个用户，如果存在则校验密码
                userToLogin = User.query.filter(User.username == userName).first()
                print "userToLogin: %s" % userToLogin

                #判断用户是否存在db中
                if userToLogin: #如果数据库中有这个user，则校验密码是否正确
                    passwordResult = util.validateMd5Password(userPassword, userName)  # 验证发过来的密码是否和用户存在db里的密码加密后相等
                    if passwordResult: # 如果密码正确，处理token和loginTime
                        #先把用户的token取出来
                        userTokenInDB = userToLogin.token
                        print "userTokenInDB: %s" %userTokenInDB
                        #userToken = generateUUID() if not userTokenInDB else generateUUID() #这样更简洁一些
                        # 登录的时候，把数据库里的loginTime和token都做更新
                        userToken = util.generateUUID()
                        userToLogin.token = userToken
                        timeStr = time.strftime("%Y-%m-%d %H:%M:%S")
                        userToLogin.loginTime = timeStr
                        db.session.commit()
                        return {"token": "%s" % userToken, "code": "00", "userid": int(userToLogin.id), "login_time": "%s" %timeStr}
                    else: #密码不正确
                        return {"code": "02", "message": u"参数值不合法，密码不正确"}
                else:
                    # 数据库中没有这个user
                    return {"code": "02", "message": u"参数值不合法，用户不存在"}

            else:
                return {"code": "03","message": u"参数错误，可能原因：参数少传了、多传了、写错了"}

        except Exception as e:
            print "error of login: %s" % e
            return {"code": "999","message": u"未知错误"}
