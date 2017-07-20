#!/usr/bin/python
#encoding:utf-8


'''
程序作用:处理5000多条数据,并提取当中有用的用户信息

'''


import re
import chardet
import sys
reload(sys)
sys.setdefaultencoding('utf8')

#循环打开所有文件
#正则匹配需要的内容

for i in range(1,5583):
    i = str(i)
    file = open(i,'r')
    data = file.read().decode('gbk')
    #print data

    file.close()

    userid = re.findall('name="userid"  value=(.*?)/> ',data,re.S)

    usercode = re.findall('name="usercode"  value=(.*?)/> ',data,re.S)
    username = re.findall('name="username"  value=(.*?)/> ', data, re.S)
    username = str(username)
    phonedata = re.findall("<td class='inputname'>(.*?)/>", data, re.S)
    phonedata = '/'.join(phonedata) #将列表转换为字符串

    phone = re.findall("value=\"(.*?)\"", phonedata, re.S)[0]

    userid = '/'.join(userid).strip("\"")
    usercode = '/'.join(usercode).strip("\"")
    phone = '/'.join(phone).replace("/","")

    username = username.decode('unicode-escape').encode('utf-8')


    file = open('100.txt','a')
    file.write(userid+usercode+username+phone+"\n")
    file.close()

    #usercode = re.findall(,data,re.S)
