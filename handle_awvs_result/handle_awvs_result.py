# -*- coding:utf-8 -*-
__author__ = 'jerry'



import xml.etree.ElementTree as ET
import re
global StartUrl
StartUrl=''



file = open('export.xml','r')
data = file.read()  #type(data)为str
file.close()


def get_starturl(data):
	global StartUrl
	starturl = re.findall('''<Crawler StartUrl="(.*?)">''', data, re.S)
	starturl = str(starturl[0])
	StartUrl = starturl



#数据分组成list,转化为str,
def divide_data(data):
	global StartUrl
	datalist = re.findall("<SiteFile id=.*?</SiteFile>", data, re.S)

	for eachdata in datalist:
		eachdata = str(eachdata)
		#print eachdata

		handle_data(eachdata)


#处理数据,获取数据
# StartUrl:起始地址 Dir1:1级文件夹 Dir2:2级文件夹 Dir3:3级文件夹 DirLen:目录深度
# FileName:文件名  OthersDir:超过3级后的所有路径
# GVariation1,GVariation2:get方式的变量 PVariation1,PVariation2:post方式的变量  PValue1:post过去的值
#原数据中URl代表相对URL,FULLURL为绝对路径的URL

def handle_data(element_data):

	global StartUrl
	#初始化一个字典,用来装载数据
	sitefile ={ "StartUrl":StartUrl,
				"FileName":"",
	            "URL":"",
	            "FullURL":"",
	            "Dir1":"",
	            "Dir2":"",
	            "Dir3":"",
	            "DirLen":"",
	            "GVariation1": "",
	            "GVariation2": "",
	            "PVariation1": "",
	            "PVariation2": "",
	            "PValue1": "",
	            "PValue2": "",
	            "OthersDir":""
				}

	# 用ElementTree解析
	dom = ET.fromstring(element_data)

	# 获取Name的值,即文件名,有三种情况 None,含有.,没含有.
	for elem in dom.iter(tag='Name'):
		try:
			if '.' in elem.text: # 如果含有.则是文件
				sitefile["FileName"] = elem.text
		except:
			sitefile["FileName"] =''

	# 获取URL的值
	#for elem in dom.iter(tag='URL'):
		#sitefile["URL"] = elem.text

	# 获取变量和变量值
	# 处理element_data
	variationsdata = re.findall("<Variations>(.*?)</Variations>", element_data, re.S)
	#print variationsdata
	variationsdata = str(variationsdata)

	#对含有变量的data进行处理
	if '<Variation>' in variationsdata:   #如果postdata内有变量的话
		urldatalist = re.findall("\<URL\>(.*?)\<\/URL\>", variationsdata, re.S)
		# print zero_num
		#print urldatalist
		url_num = len(urldatalist)
		#print url_num

		postdatalist = re.findall("<\!\[CDATA\[(.*?)\]\]>", variationsdata, re.S)
		#print postdatalist
		postdata_num = len(postdatalist)

		# 统计有几个为空的postdata
		zero_num = postdatalist.count('')

		#遍历Url列表中的url
		for i in range(1,postdata_num+1):
			if postdatalist[i-1] =='': #post数据为0,则为get方式
				sitefile["GVariation%d"%i] = urldatalist[i-1].split('?')[-1]
			else:
				sitefile["PVariation%d" % (i-zero_num)] = urldatalist[i-1].split('?')[-1]
				sitefile["PValue%d" % (i-zero_num)] = postdatalist[i-1]

		#print Variations_dic
		#print '--------'


		# 给变量赋值

	else:
		pass

	'''
	if '?' in sitefile["URL"]:
		temp = sitefile["URL"] #<type 'str'>
		sitefile["Variation"] = temp.split('?')[-1]
	'''


	# 获取FULLURL的值
	for elem in dom.iter(tag='FullURL'):
		sitefile["FullURL"] = elem.text

	#获取 DirLen
	fullurl = sitefile["FullURL"]
	fullurl = fullurl.split('/')
	#print fullurl
	sitefile["DirLen"] = len(fullurl)-4

	others_str = ''

	# 获取 Dir1:1级文件夹 Dir2:2级文件夹 Dir3:3级文件夹
	if sitefile["DirLen"] == 0:
		sitefile["Dir1"] =''
	elif sitefile["DirLen"] == 1:
		sitefile["Dir1"] = fullurl[3]
	elif sitefile["DirLen"] == 2:
		sitefile["Dir1"] = fullurl[3]
		sitefile["Dir2"] = fullurl[4]
	elif sitefile["DirLen"] == 3:
		sitefile["Dir1"] = fullurl[3]
		sitefile["Dir2"] = fullurl[4]
		sitefile["Dir3"] = fullurl[5]
	else:
		sitefile["Dir1"] = fullurl[3]
		sitefile["Dir2"] = fullurl[4]
		sitefile["Dir3"] = fullurl[5]

		others = fullurl[6:-1]
		for each in others:
			others_str = others_str + '/' + str(each)
		sitefile["OthersDir"] = others_str


	print sitefile

'''
	print sitefile["GVariation1"]
	print sitefile["GVariation2"]
	print sitefile["PVariation1"]
	print sitefile["PVariation2"]
	print sitefile["PValue1"]
	print sitefile["PValue2"]
	print '******************'
'''
	#print sitefile['']
	#print sitefile["URL"]

	#for elem in dom.iter(tag='Variable'):
		#print elem.attrib




if __name__ == '__main__':

	get_starturl(data)
	divide_data(data)
