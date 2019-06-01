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
import re

# 查询用户的博文接口
class GetBlogsContent(Resource):
    # def __init__(self):
    #     self.reqparse = reqparse.RequestParser()
    #     self.args = self.reqparse.parse_args()

    #处理查询用户的博文接口
    def get(self, articleIdString):
        try:
            print "articleIdString: %s" % articleIdString
            # 用正则匹配articleIds=1,2,3中等号后面的部分
            reMatchResult = re.match(r"articleIds=(.*)", articleIdString)
            # 如果匹配到了，说明传了articleIds=部分，继续取articleId
            if reMatchResult:
                articleIdResultString = reMatchResult.group(1)
                print "articleIdResultString: %s" % articleIdResultString

                # 判断articleIds=后边的id是否有传，传了就把所有的id取出来
                if articleIdResultString:
                    articleIdList = articleIdResultString.split(',')
                    print "articleIdList: %s" % articleIdList
                    responseDict = {"code": "00", "data": []}
                    blogList = []  # 用于存查询到的blog

                    # 遍历articleIdList，判断每个id是否在db里存在
                    for id in articleIdList:
                        # 校验id值的类型，把字符型转为整形
                        try:
                            idValue = int(id)
                        # 如果不能专属数字，提示不是数字
                        except:
                            return {"code": "02", "message": u"参数值不合法，articleId: %s 不是数字" % id}
                        blog = UserBlog.query.filter(UserBlog.articleId == idValue).first()
                        # 如果这个id有，则把blog对象存到blogList里
                        if blog:
                            blogList.append(blog)
                        # 如果这个id没有，则提示参数值错误
                        else:
                            return {"code": "02", "message": u"参数值不合法，不存在articleId: %s " % id}
                    # 获取到的blog都存到blogList后，把blog填充到responseDict
                    responseDictFilled = util.fillInResponseDict(responseDict, blogList)
                    return responseDictFilled
                # 没有传后边的id，则提示articleId没有传articleIdResultString
                else:
                    return {"code": "02", "message": u"参数值不合法，articleId没有传"}
            # 没匹配到，提示articleIds=没有传值
            else:
                return {"code": "02", "message": u"参数值不合法，articleIds=没有传值"}

        except Exception as e:
            print "error of getBlogContent: %s" % e
            return {"code": "999", "message": u"未知错误"}
