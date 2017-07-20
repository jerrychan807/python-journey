#!/usr/bin/python
#encoding:utf-8


import os
import json
import commands


'''
程序作用:查询版本为6,7的centos系统所有网卡配置信息,并返回json格式的数据

'''

def return_dns_list_json_result():
    # 初始化一个字典,存放dns数据信息的容器
    dns_list = {}

    dns_output = os.popen("cat /etc/resolv.conf")
    dns_no = 1 # DNS序号

    for line in dns_output:
        if 'nameserver' in line:
            temp = line.strip('\n').split(' ')[-1]
            dns_list['DNS%d'%dns_no] =temp
            #dns_list.append(temp)
            dns_no +=1
    dns_list = dns_list
    dns_list_json = json.dumps(dns_list)
    #print type(dns_list_json)
    #print dns_list_json
    dns_list_json_result = "\"DNS\":" + dns_list_json
    return dns_list_json_result




def return_eth_config_json_result():
    list=[]
    json_dictlist=[]
    json_dict=''

    #初始化装载 json格式的配置信息容器
    eth_config_list_json_result = ''

    #定义需要在配置文件中匹配的参数列表
    parameter_list=['DEVICE','IPADDR','NETMASK','GATEWAY']

    #初始化一个字典,作为存放网卡配置的信息的容器
    eth_infomatoin_dict = {}

    #网卡配置所在路径 /etc/sysconfig/network-scripts/
    #读取DEVICE(name),IPADDR(ip),NETMASK,GATEWAY

    #获取所有符合条件的文件名,数据类型为str
    (status,allfilename) = commands.getstatusoutput("ls /etc/sysconfig/network-scripts/ | grep '^ifcfg.*[0-9.*]$'")




    #以换行符为分割,将所有文件名混合在一起的字符串分割为几个单独文件名
    #filename = ['ifcfg-eth0','ifcfg-eth1','ifcfg-eth2']
    filename = allfilename.split("\n")


    for eachfile in filename: #遍历配置文件名
        eth_infomatoin_output = os.popen('cat /etc/sysconfig/network-scripts/'+ eachfile) #输出对应文件名内的配置信息
        for line in eth_infomatoin_output: #遍历每行配置项
            for parameter in parameter_list: #如果含有某些参数就继续执行
                if parameter in line:
                    temp = line.strip('\n').split('=') #去掉末尾换行符,以等号分割
                    #json_dict[parameter] = temp[0]
                    value =  temp[-1] # 取等号右边的数值信息
                    eth_infomatoin_dict[parameter] =value.strip("\"")

        #将每个网卡的配置信息转换成json格式
        jsontemp = json.dumps(eth_infomatoin_dict)
        json_dict = "\""+"%s\":"%eachfile+jsontemp
        json_dictlist.append(json_dict)

    for i in range(0,len(json_dictlist)):
        tmp =  json_dictlist[i]+ ','
        eth_config_list_json_result = eth_config_list_json_result + tmp

    return eth_config_list_json_result


def output_result(eth_result,dns_result):
    result = ''
    result = eth_result + dns_result
    result = '{'+result+'}'
    print result




if __name__ == '__main__':
    eth_config_json_result = return_eth_config_json_result()
    dns_list_json_result = return_dns_list_json_result()

    output_result(eth_config_json_result,dns_list_json_result)
