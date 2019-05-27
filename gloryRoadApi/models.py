#encoding=utf-8

from datetime import datetime
from gloryRoadApi import db

#定义用户表模型类User，用来存储用户信息（id、username、password、email、token、loginTime）
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    password = db.Column(db.String(200))
    email = db.Column(db.String(20))
    token = db.Column(db.String(50),default = None)
    loginTime = db.Column(db.String(40), default = None)
    blogs = db.relationship('UserBlog', back_populates = 'user')# 定义blogs关联属性，用来关联有多少个博客

    def __repr__(self):
        # %r是用repr()方法处理对象，返回类型本身，而不进行类型转化
        return '<table User=> id: %d username:%r password:%r email:%r token : %r loginTime:%r>' % \
               (self.id, self.username, self.password,self.email, self.token, self.loginTime)

#定义博文表模型类UserBlog，用来存储用户信息（id、username、password、email、token、loginTime）
class UserBlog(db.Model):
    articleId = db.Column(db.Integer, primary_key=True)
    blogTitle = db.Column(db.Text)
    blogContent = db.Column(db.Text)
    '''定义外键，用来做关联关系映射，其中“表名.字段名”中的表名是数据库中实际的表名，为小写
    （模型类对应的表名由Flask-SQLAlchemy生成，默认为类名称的小写形式）'''
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    createTime = db.Column(db.String(100), default = None) # 创建博文的时间
    updateTime = db.Column(db.String(100), default = None) # 更新博文的时间
    user = db.relationship('User', back_populates = 'blogs') #定义user关系属性，用来关联博客属于哪个user

    def __repr__(self):
        # %r是用repr()方法处理对象，返回类型本身，而不进行类型转化
        return '<table UserBlog=> articleId: %d blogTitle:%r blogContent:%r user_id:%d createTime : %r updateTime : %r>' % \
               (self.articleId, self.blogTitle, self.blogContent,self.user_id, self.createTime, self.updateTime)














