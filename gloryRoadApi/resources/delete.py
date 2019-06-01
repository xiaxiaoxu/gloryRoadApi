#encoding=utf-8

#encoding=utf-8
from gloryRoadApi import app, db
from gloryRoadApi.models import User, UserBlog
# from gloryRoadApi.commands import forge,initdb
from flask_restful import Resource, Api
import time
from flask_restful import reqparse
from flask_restful import request
from flask_restful import fields, marshal_with
from gloryRoadApi.common import util
from gloryRoadApi.common.log import info, error,warning
import json
# 查询用户的博文接口
class Delete(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('userid', type = int, help =u"userid输入错误", location = 'json' )
        self.reqparse.add_argument('token', type = str, help= u"token校验错误", location = 'json')
        self.reqparse.add_argument('articleId', type = list, location = 'json')
        self.args = self.reqparse.parse_args()

    #处理查询用户的博文接口
    def delete(self):
        try:
            userid = self.args['userid']
            userToken = self.args['token']
            articleIdList = self.args['articleId']
            neededParams = self.args.keys()  # 记录self.reqparse.add_argument中添加的参数列表
            print "neededParams:", neededParams
            requestParams = request.json.keys()  # 记录发送请求中携带的参数列表
            print "requestParams:", requestParams
            requestTimestamp = time.time()

            # 校验是否参数都有传过来，不多不少
            if userid and userToken and articleIdList and util.paramsNumResult(neededParams, requestParams):
                getUserInDB = User.query.filter(User.id == userid).first()
                print "getUserInDB: %s" %getUserInDB
                # 如果用户存在，判断登录时间是否超过一小时
                if getUserInDB:
                    userLoginTime = getUserInDB.loginTime #取出用户的登录时间
                    print "userLoginTime: %s" % userLoginTime
                    # 校验登录时间是否超过1小时
                    if util.calculateTimeDiff(userLoginTime, requestTimestamp) >= 1:
                        return {"code": "02", "message": u"参数值不合法，token已过期，请重新登录"}
                    # 登录时间没超过1小时,继续校验token是否和useid是否相匹配
                    else:
                        # 获取用户在DB中的token
                        userTokenInDB = getUserInDB.token
                        print "userTokenInDB: %s" % userTokenInDB
                        # 判断token和userid是否相匹配，匹配则处理articleIdList列表
                        if userToken == userTokenInDB:
                            # 判断articleIdList的值是否为列表，是的话，则遍历列表继续处理
                            if type(articleIdList) == list:
                                print "articleIdList: %s" % articleIdList
                                # 遍历articleId列表
                                for id in articleIdList:
                                    # 用id去找blog
                                    blog = UserBlog.query.filter(UserBlog.articleId == id).first()
                                    # 能找到，说明id存在，进行删除动作
                                    if blog:
                                         # 先从db session中删掉，最后一起commit
                                         db.session.delete(blog)

                                    # 没找到，说明id不存在，提示参数值不合法
                                    else:
                                        return {"code": "02", "message": u"参数值不合法，articleId：%s 不存在" % id}
                                # 遍历完articleIdList，id都存在，且都做了删除，则提交commit
                                db.session.commit()
                                #数据库提交删除后，返回结果
                                return json.dumps({"userid": userid, "token": userToken, "articleId": articleIdList})

                            # articleId的值不是列表，提示articleId传的不是列表
                            else:
                                return {"code": "02", "message": u"参数值不合法，articleId传的不是列表"}

                        # token和userid不匹配，说明token不正确，返回参数值不合法，token不正确
                        else:
                            return {"code": "02", "message": u"参数值不合法，token不正确"}
                # 如果用户不存在，提示参数值不合法，用户不存在
                else:
                    return {"code": "02", "message": u"参数值不合法，用户不存在"}
            # 参数没传全，或参数写错了，或参数多了
            else:
                return {"code": "03", "message": u"参数错误，可能原因：参数少传了、多传了、写错了、值为空"}

        except Exception as e:
            print "error of delete: %s" % e
            return {"code": "999", "message": u"未知错误"}
