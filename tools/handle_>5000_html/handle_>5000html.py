#!/usr/bin/python
#encoding:utf-8
__author__ = 'jerry'


'''
程序作用:处理5000多条数据,并提取当中有用的用户信息

'''


import re
import sys
from prettytable import PrettyTable




reload(sys)
sys.setdefaultencoding('utf8')



#循环打开所有文件
#正则匹配需要的内容
table_output = PrettyTable(["userid", "usercode", "username", "phone"])
table_output.align["userid"] = "l"
table_output.padding_width = 1

for i in range(1,5583):
    i = 'data/' + str(i)
    file = open(i,'r')
    data = file.read().decode('gbk')
    #print data

    file.close()

    #获取userid
    userid = re.findall('name="userid"  value=(.*?)/> ',data,re.S)

    #获取usercode
    usercode = re.findall('name="usercode"  value=(.*?)/> ',data,re.S)

    #获取username
    username = re.findall('name="username"  value=(.*?)/> ', data, re.S)


    #获取phone
    phonedata = re.findall("<td class='inputname'>(.*?)/>", data, re.S)
    phonedata = '/'.join(phonedata) #将列表转换为字符串
    phone = re.findall("value=\"(.*?)\"", phonedata, re.S)[0]


    #清理数据
    userid = userid[0].replace("\""," ")

    usercode = usercode[0].replace("\""," ")

    phone = '/'.join(phone).replace("/","")

    username = str(username[0]).replace("\""," ")
    username = username.encode('utf-8')
    table_output.add_row([userid,usercode, username, phone])


print table_output


    #file = open('result.txt','a')
    #file.write(userid + ' ' + usercode + ' ' + username + ' ' + phone + "\n")
    #file.close()

