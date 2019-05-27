#encoding=utf-8
import re
import hashlib
import time
from gloryRoadApi import app, db
from gloryRoadApi.models import User
import re
# md5加密方法
import hashlib
import os
import uuid



# 正则验证email
def validateEmail(emailStr):
    p = re.compile(r'^[a-zA-Z0-9\.]+@[a-zA-Z0-9]+\.[a-zA-Z]{3}$')
    if p.match(emailStr):
        return True
    else:
        return False

# 正则验证username
def validateUsername(username):

    # if re.compile(u'[\u4e00-\u9fa5]',username):
    #     print "has chinese"
    if re.match(r'\w+', username) and (len(username) in range(2, 21)):
        #print type(username)
        return True
    else:
        return False

# 正则验证email格式
def validatePassword(password):
    if re.search(r'[a-zA-Z]+', password) and re.search(r'[\d+]', password) and (len(password) in range(2, 21)):
        return True
    else:
        return False

# 验证请求中的参数是否有要求之外的，如果有，返回False
def paramsNumResult(neededParams, requestParams):
    for param in requestParams:
        if param not in neededParams:
            print "param not in needed params:", param
            return False
    return True



# md5加密方法，用于调试
def md5Hash(password):
    """md5 加密分为digest和hexdigest两种格式，前者是二进制，后者是十六进制格式，这里默认为十六进制"""
    try:
        m5 = hashlib.md5()
        m5.update(password)
        pwd = m5.hexdigest()
        return pwd
    except Exception, e:
        print  "md5Hash error: %s" % e

#判断两个字符串用md5加密后是否相等，用于调试
import hashlib

def compareMd5Pwd(str1, str2):
    md51 = hashlib.md5()
    md51.update(str1)
    pwd1 = md51.hexdigest()
    print "pwd1: %s" % pwd1
    md52 = hashlib.md5()
    md52.update(str2)
    pwd2 = md52.hexdigest()
    print "pwd2: %s" % pwd2
    return True if (pwd1 == pwd2) else False
    #print "pwd1 = pwd2" if (pwd1 == pwd2) else "pwd1 != pwd2"


# 登录接口发送的密码是md5加密的，需要从数据库里找到这个username对应的password，进行加密后和用户发送的加密串是否一致
def validateMd5Password(passwordFromPost,usernameFromPost):
    try:
        print "passwordFromPost: %s" % passwordFromPost
        print "usernameFromPost: %s" % usernameFromPost
        userInDb = User.query.filter(User.username == usernameFromPost).first()
        print "userInDb: %s" %userInDb
        if userInDb:
            passwordInDb = userInDb.password
            print "passwordInDb: %s" % passwordInDb
            passwordInDbMd5 = md5Hash(passwordInDb)
            print "passwordInDbMd5: %s" % passwordInDbMd5
        else:
            passwordInDbMd5 = None
            print "passwordInDbMd5: %s" % passwordInDbMd5

        if passwordFromPost == passwordInDbMd5:
            return True
        else:
            return False

    except Exception, e:
        print "validateMd5Password Error: %s " %e


# 验证用户名是否在数据库中存在
def validateUsernameExistInDB(userName):
    try:
        if User.query.filter(User.username == userName).all(): # 查询数据库里是否存在userName
            return True
        else:
            return False
    except Exception,e:
        print "error : %s" % e

#生成uuid，用uuid模块的uuid4()方法
def generateUUID():
    try:
        uuidStr = uuid.uuid4().hex
        return uuidStr
    except Exception, e:
        print "uuidGenerate Error :%s" %e


#计算时间差（单位：小时）
#第一个参数传入数据库里用户的登录时间字符串，第二个参数是当前时间戳
def calculateTimeDiff(userLoginTimeStr, timestamp):
    try:
        timestampNew = timestamp
        print "timestampNew : time when post request: %s" % timestampNew
        timeArray = time.strptime(userLoginTimeStr, "%Y-%m-%d %H:%M:%S") # 把userLogin时间字符串转成时间元祖
        print "timeArray after time.strptime func: %s" %timeArray
        timestampOld = time.mktime(timeArray) # 把时间元祖转换成时间戳
        print "timestampOld format from timeArray: %s" % timestampOld
        timeStampDiff = timestampNew - timestampOld # 两个时间戳相减，得出时间差（单位：秒）
        print "timeStampDiff: %s" % timeStampDiff

        if timeStampDiff > 0:
            timeHourDiff = int(divmod(timeStampDiff,3600)[0]) # 把时间差（秒）换算成小时，处理3600，得到一个元祖，第一个值为小时
            print "the time difference is : %s hour" % timeHourDiff
            return timeHourDiff
        else:
            print "timestamp different is negative"
            return "wrong"
    except Exception, e:
        print "calculate time difference error: %s" % e