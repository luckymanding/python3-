# -*- coding:utf-8 -*-
import urllib.request
import urllib.error
import re

class BDTB:
	def __init__(self,baseUrl,seeLZ,floorTag):
		self.baseURL=baseUrl
		self.seeLZ='?see_lz='+str(seeLZ)
		self.tool=Tool()
		self.file=None
		self.floor=1
		self.defaultTitle="百度贴吧"
		self.floorTag=floorTag

	def getPage(self,pageNum):
		try:
			url=self.baseURL+self.seeLZ+'&pn='+str(pageNum)
			req=urllib.request.Request(url)
			response=urllib.request.urlopen(req)
		#	print(response.read().decode('utf-8'))
			return response.read().decode('utf-8')
		except urllib.error.URLError as e:
			if hasattr(e,"reason"):
				print("连接百度贴吧失败，错误原因"+e.reason)
				return None

	def getTitle(self,contens):	
		pattern=re.compile('<h3.*?>(.*?)</h3>')
		result=re.search(pattern,str(contens))
		if result:
			return result.group(1).strip()
		else:
			return None

	def getpageNum(self,content):
		pattern=re.compile('<li class="l_reply_num.*?</span>.*?<span.*?>(.*?)</span>')
		result=re.search(pattern,content)
		if result:
			return result.group(1).strip()
		else:
			return None

	def getContent(self,page):
		pattern=re.compile('<div id="post_content_.*?>(.*?)</div>',re.S)
		items=re.findall(pattern,page)
		contents=[]
		for item in items:
			content="\n"+self.tool.replace(item)+"\n"
			contents.append(content)
		return contents

	def setFilename(self,title):
		if title is not None:
			self.file=open(title+".txt","w+")
		else:
			self.file=open(self.defaultTitle+".txt","w+")

	def writeData(self,contents):
		for item in contents:
			if self.floorTag=="1":
				floorLine="\n"+str(self.floor)+"------------------------------------------------------------------------------"+"\n"
				self.file.write(floorLine)
			self.file.write(str(item))
			self.floor+=1


	def start(self):
		indexPage=self.getPage(1)
		pageNum=self.getpageNum(indexPage)
		title=self.getTitle(indexPage)
		self.setFilename(title)
		if pageNum==None:
			print("URL已失效,请重试")
			return
		try:
			print("该帖子共有"+str(pageNum)+"页")
			for i in range(1,1+int(pageNum)):
				print("正在写入第"+str(i)+"页数据")
				page=self.getPage(i)
				contents=self.getContent(page)
				#print(contents)
				self.writeData(contents)

		except IOError as e:
			print("写入异常，原因"+e.message)
		finally:
			print("写入任务完成")


class Tool:
	removeImg=re.compile('<img.*?>| {7}|')
	removeAddr=re.compile('<a.*?>|</a>')
	replaceLine=re.compile('<tr>|<div>|</div>|</p>')
	replaceTD=re.compile('<td>')
	replacePara=re.compile('<p.*?>')
	replaceBR=re.compile('<br><br>|<br>')
	removeExtraTag=re.compile('<.*?>')
	def replace(self,x):
		x=re.sub(self.removeImg,"",x)
		x=re.sub(self.removeAddr,"",x)
		x=re.sub(self.removeExtraTag,"",x)
		x=re.sub(self.replaceLine,"\n",x)
		x=re.sub(self.replaceTD,"\t",x)
		x=re.sub(self.replacePara,"\n",x)
		x=re.sub(self.replaceBR,"\n",x)
		return x.strip()
'''
bdtb=BDTB("http://tieba.baidu.com/p/3138733512",1,1)
A=bdtb.getPage(1)

print(bdtb.getContent(A))
'''

	

print("请输入帖子代号")
baseURL='http://tieba.baidu.com/p/'+str(input("http://tieba.baidu.com/p/"))
seeLZ=input("是否只读取楼主发言，是输入1，否输入0\n")
floorTag=input("是否写入楼层信息，是输入1，否输入0\n")
bdtb=BDTB(baseURL,seeLZ,floorTag)
bdtb.start()

