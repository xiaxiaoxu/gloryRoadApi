#encoding=utf-8

#encoding=utf-8
from gloryRoadApi import app, db
from gloryRoadApi.models import User, UserBlog
# from gloryRoadApi.commands import forge,initdb
from gloryRoadApi.common.log import info, error,warning
from flask_restful import Resource, Api
import time
from flask_restful import reqparse
from flask_restful import request
from flask_restful import fields, marshal_with
from gloryRoadApi.common import util

# 查询用户的博文接口
class GetBlogsOfUser(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('userid', type = int, help =u"userid输入错误", location = 'json' )
        self.reqparse.add_argument('token', type = str, help= u"token校验错误", location = 'json')
        self.reqparse.add_argument('offset', type = int, location = 'json')
        self.reqparse.add_argument('lines', type = int, location = 'json')
        self.args = self.reqparse.parse_args()

    #处理查询用户的博文接口
    def post(self):
        try:
            userid = self.args['userid']
            userToken = self.args['token']
            offset = self.args['offset']
            lines = self.args['lines']
            neededParams = self.args.keys()  # 记录self.reqparse.add_argument中添加的参数列表
            print "neededParams:", neededParams
            requestParams = request.json.keys()  # 记录发送请求中携带的参数列表
            print "requestParams:", requestParams
            requestTimestamp = time.time()
            print "type(offset) -> %s \n type(lines) -> %s" %(type(offset), type(lines))

            # 校验是否参数都有传过来(除了offset和lines)，不多不少
            if userid and userToken and util.paramsNumResult(neededParams, requestParams):
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
                        # 判断token和userid是否相匹配，匹配则处理offset和lines逻辑
                        if userToken == userTokenInDB:
                            # 定义一个临时字典
                            responseDict = {"data": [], "code": "00", "userid": userid}
                            userOfBlog = User.query.filter(User.id == userid).first()
                            blogs = userOfBlog.blogs
                            print "blogs:", blogs
                            # 如果用户有博文，则继续，否则直接返回responseDict
                            if blogs:
                                # 如果offset和lines都传了则继续校验offset和lines的值
                                if offset and lines:
                                    # 判断博文数是否够跳offset条，够跳，继续判断是否够返回lines条数据
                                    if len(blogs) > int(offset):
                                        # 跳过offset够取lines条数据，返回跳过offset条后，lines条数据：blogs[offset : (offset + lines + 1)]，包含第lines条
                                        if (len(blogs) - int(offset)) > int(lines):
                                            blogsAfterJumpOffsetGetLines = blogs[int(offset) : (int(offset) + int(lines))]
                                            print "blogsAfterJumpOffsetGetLines : %s" % blogsAfterJumpOffsetGetLines
                                            responseDictFilled = util.fillInResponseDict(responseDict, blogsAfterJumpOffsetGetLines)
                                            return responseDictFilled
                                        # 跳过offset不够取lines条数据，返回跳过offset条后所有的blog：blogs[offset : ]
                                        else:
                                            blogsAfterJumpOffset = blogs[int(offset) : ]
                                            print "blogsAfterJumpOffset: %s" % blogsAfterJumpOffset
                                            responseDictFilled = util.fillInResponseDict(responseDict, blogsAfterJumpOffset)
                                            return responseDictFilled

                                    # 博文数不够跳offset条，则返回博文列表为空
                                    else:
                                        return responseDict
                                # offset和lines没有都传过来，则返回用户全部博文
                                else:
                                    responseDictFilled = util.fillInResponseDict(responseDict, blogs)
                                    return responseDictFilled
                            # 没有博文，直接返回，"data"列表为空
                            else:
                                return responseDict

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
            print "error of update: %s" % e
            return {"code": "999", "message": u"未知错误"}
