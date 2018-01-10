import urllib.request
import urllib.error
import re

class QSBK:
	def __init__(self):
		self.pageIndex=1
		self.user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36"
		self.header={'User-Agent':'self.user_agent'}
		self.stories=[]
		self.enable=False

	def getPage(self,pageIndex):
		try:
			url='https://www.qiushibaike.com/hot/page/'+str(pageIndex)
			req=urllib.request.Request(url,headers=self.header)
			response=urllib.request.urlopen(req)
			pageCode=response.read().decode('utf-8')
			return pageCode
		except urllib.error.URLError as e:
			print("getPage失败")
			if hasattr(e,"code"):
				print(e.code)
			if hasattr(e,"reason"):
				print(e.reason)
	def getPageItems(self,pageIndex):
		pageCode=self.getPage(pageIndex)
		if not pageCode:
			print("页面加载失败...")
			return None
		pattern = re.compile('''<div class="article.*?<h2>(.*?)</h2>'''
							 + '''.*?<a href="(.*?)"'''
							 + '''.*?<span>(.*?)</span>'''
							 + '''.*?<!-- 图片或gif -->(.*?)<div class="stats">'''
							 + '''.*?<span class="stats-vote"><i class="number">(.*?)</i>''', re.S)
		items = re.findall(pattern, pageCode)
		pageItems = []
		for item in items:
			# 如果段子中没有图片，保存段子
			if not re.search("img", item[3]):
				# 如果已经显示了段子的全部内容
				# print(item.group())
				if not re.search("查看全文", item[3]):
					result = re.sub("<br/>", "\n", item[2])
					pageItems.append([item[0].strip(), result.strip(), item[4].strip()])
				# 没有显示全部内容，通过item[1]发起请求访问段子的全部内容
				else:
					contentForAll = self.getPage(contentUrl=item[1])
					# ForAll页面的正则表达式是之前的不太相同
					patternForAll = re.compile('''<div class="article.*?<h2>(.*?)</h2>'''
											   + '''.*?<div class="content">(.*?)</div>'''
											   + '''.*?<span class="stats-vote"><i class="number">(.*?)</i>''', re.S)
					itemForAll = re.findall(patternForAll, contentForAll)
					result = re.sub("<br/>", "\n", itemForAll[1])
					pageItems.append([itemForAll[0].strip(), result.strip(), itemForAll[2].strip()])
		return pageItems
		

	def  loadPage(self):
		if self.enable==True:
			if len(self.stories)<2:
				pageItems=self.getPageItems(self.pageIndex)
				if pageItems:
					self.stories.append(pageItems)
					self.pageIndex+=1

	def getOneStory(self,pageStories,page):
		for story in pageStories:
			receive=input()
			self.loadPage()
			if receive=="Q":
				self.enable=False
				return
			print("当前第:%s页\n发布人:%s\n内容:%s\n点赞数:%s\n" % (page, story[0], story[1], story[2]))

	def start(self):
		self.enable=True
		self.loadPage()
		nowPage=0
		while self.enable:
			if len(self.stories)>0:
				pageItems=self.stories[0]
				nowPage+=1
				del self.stories[0]
				self.getOneStory(pageItems,nowPage)

if __name__=="__main__":
	spider=QSBK()
	spider.start()
	


