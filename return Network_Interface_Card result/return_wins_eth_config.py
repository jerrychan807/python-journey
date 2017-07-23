# -*- coding:utf-8 -*-
__author__ = 'jerry'

import re
import json
import sys

reload(sys)
sys.setdefaultencoding('utf8')

#定义一个全局变量 用来存放所有的dns记录
global DNS_LIST
DNS_LIST =[]


#处理ifconfig/all输出的信息,截取3个网卡部分的内容列表
def get_eth_info():
    file = open('1.txt','r')
    data = file.read().decode('gbk')  #data的编码格式为unicode
    file.close()

    PATTERN = ur'以太网适配器([\s\S]*?)NetBIOS' #PATTERN的编码格式为unicode
    pattern = re.compile(PATTERN)

    #re.S：.将会匹配换行符，默认.逗号不会匹配换行符
    #分割data,分成3部分,一个网卡为一部分
    eth_info_list = pattern.findall(data,re.S)
    return eth_info_list


#获取某个网卡的所有信息,提取当中的eth_name,netmask,ip_address,gateway信息
def get_element(info):
    global DNS_LIST

    eth_info= info  #eth_info为<type 'unicode'>
    #print eth_info

    eth_name_pattern = ur'本地连接([\s\S]*?)\:'
    eth_name = re.search(eth_name_pattern,eth_info).group(1).strip(' ')
    if eth_name =='':
        eth_name = '1'
    else:
        eth_name = eth_name.encode('utf-8')

    eth_name = 'eth' + eth_name
    #print eth_name


    # 抓取ip地址字段
    ip_pattern = ur'IPv4([\s\S]*?)\(首选'
    ip_address = re.search(ip_pattern,eth_info).group(1)

    ip_address = ip_address.split(':')[-1].strip(' ')
    if len(ip_address) < 3:
        ip_address = '0'
    else:
        ip_address = ip_address.encode('utf-8')
    #print 'ip:' + ip_address

    #抓取子网掩码字段
    netmask_pattern = ur'子网掩码([\s\S]*?)默认网关'
    netmask = re.search(netmask_pattern, eth_info).group()
    netmask = netmask.split(':')[-1]
    netmask = netmask.split('\n')[0].strip('\r ')
    netmask = netmask
    if len(netmask) < 3:
        netmask = '0'
    else:
        netmask = netmask.encode('utf-8')
    #print 'netmask:' + netmask


    # 抓取默认网关字段
    gateway_pattern = ur'默认网关([\s\S]*?)DNS'
    gateway = re.search(gateway_pattern,eth_info).group(1)
    gateway = gateway.split(':')[-1]
    gateway = gateway.split('\n')[0]

    if len(gateway)<3:
        gateway = '0'
    else:
        gateway = gateway.strip('\r ').encode('utf-8')
    #print 'gateway' + gateway


    #抓取dns字段
    dns_pattern = ur'服务器([\s\S]*?)TCPIP'
    dns = re.search(dns_pattern, eth_info).group(1) #<type 'unicode'>

    reip = re.compile(r'(?<![\.\d])(?:\d{1,3}\.){3}\d{1,3}(?![\.\d])')
    dns = reip.findall(dns)

    for each in dns:
        each = each.encode('utf-8')
        DNS_LIST.append(each)

    #定义字典
    eth_info_dict_son = {}

    eth_info_dict_son["DEVICE"] = eth_name
    eth_info_dict_son["NETMASK"] = netmask
    eth_info_dict_son["IPADDR"] = ip_address
    eth_info_dict_son["GATEWAY"] = gateway


    eth_info_dict_dad = {}
    eth_info_dict_dad[eth_name] =  eth_info_dict_son
    #print eth_info_dict_dad

    #eth_info_dict_dad的格式{'eth3': {'DEVICE': 'eth3', 'NETMASK': '255.255.255.0', 'IPADDR': '3.3.3.11', 'GATEWAY': '0'}}
    return eth_info_dict_dad


# 列表去重函数
def remove_repeat(list):
    newlist = []
    for rep in list:
        if rep not in newlist:
            newlist.append(rep)
    return newlist


# 返回DNS记录
def return_dns_dict():
    global DNS_LIST

    # DNS列表去重
    DNS_LIST = remove_repeat(DNS_LIST)

    # dns数量
    dns_num = len(DNS_LIST)


    if dns_num == 0:  # 如果DNS数量为0
        dns1 = '0'
        dns2 = '0'

    elif dns_num == 1:  # 如果DNS数量为1
        dns1 = DNS_LIST[0]
        dns2 = '0'
    elif dns_num > 1:  # 如果DNS数量多于1
        dns1 = DNS_LIST[0]
        dns2 = DNS_LIST[1]
    else:
        pass

    dns_dict_son = {'DNS1': dns1,'DNS2': dns2}
    #print dns_dict_son
    dns_dict_dad = {'DNS':dns_dict_son}

    return dns_dict_dad


# 综合几个子字典,返回json化结果
def combine_json_result(eth_dict1, eth_dict2, eth_dict3,dnsdict):

    # 将几个子字典相加在一起，形成一个嵌套的结果字典
    eth_info_dict_result = dict(eth_dict1.items() + eth_dict2.items() + eth_dict3.items() + dnsdict.items())

    #将最终结果json化
    eth_info_json_result = json.dumps(eth_info_dict_result)

    return eth_info_json_result



if __name__ == '__main__':

    #获取网卡信息
    eth_info_list = []
    eth_info_list = get_eth_info()

    # 获取第一块网卡的信息
    first_eth_info = eth_info_list[2] #<type 'unicode'>
    first_eth_dict = get_element(first_eth_info)

    # 获取第二块网卡的信息
    second_eth_info = eth_info_list[1] #<type 'unicode'>
    second_eth_dict = get_element(second_eth_info)

    # 获取第三块网卡的信息
    third_eth_info = eth_info_list[0] #<type 'unicode'>
    third_eth_dict = get_element(third_eth_info)

    #获取dns的信息
    dnsdict = return_dns_dict()

    #json格式的最终结果
    json_result_dic = combine_json_result(first_eth_dict, second_eth_dict, third_eth_dict,dnsdict)

    print json_result_dic

