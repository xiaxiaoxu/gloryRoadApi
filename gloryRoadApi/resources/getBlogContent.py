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

# 查询用户的博文接口
class GetBlogContent(Resource):
    # def __init__(self):
    #     self.reqparse = reqparse.RequestParser()
    #     self.args = self.reqparse.parse_args()

    #处理查询用户的博文接口
    def get(self, articleId):
        try:
            # 到UserBlog模型类中找articleId的博文
            blog = UserBlog.query.filter(UserBlog.articleId == articleId).first()
            print "blog: %s" % blog
            #如果找到了blog，则返回blog
            if blog:
                return  {"code": "00", "data": [{"update_time": blog.updateTime, "title": blog.blogTitle, "content": blog.blogContent, "articleId": articleId, "owner": blog.user_id, "posted_on": blog.createTime}]}
            # 没找到blog，提示参数值不合法，articleId不存在
            else:
                return {"code": "02", "message": u"参数值不合法，articleId不存在"}


        except Exception as e:
            print "error of getBlogContent: %s" % e
            return {"code": "999", "message": u"未知错误"}
