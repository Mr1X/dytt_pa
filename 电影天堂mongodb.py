import requests
import re
import pymongo
from config import *
import threading

client = pymongo.MongoClient(MONGO_URL)		#链接数据库
db = client[MONGO_DB]

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36'}
url = 'http://www.ygdy8.net/html/gndy/dyzz/index.html'
gsem = threading.Semaphore(10)		#设置信号量为5，多线程最多5个

def get_dy_url(url):
	response = requests.get(url,headers=headers)
	response.encoding = 'gb2312'
	p = r'<a href="(.*?)" class="ulink">(.*?)</a>'
	reg = re.findall(p,response.text)
	
	for dy_url,title in reg:				#多每一个电影页面开启多线程
		threading.Thread(target=one_page,args=(dy_url,title,)).start()
		# one_page(dy_url,title)

	p = r"<a href='(.*?)'>下一页</a>"		#如果有下一页则递归爬取下一页
	reg = re.findall(p,response.text)
	if reg:
		next_url = 'http://www.ygdy8.net/html/gndy/dyzz/' + reg[0]
		print('正在爬取'+next_url)
		get_dy_url(next_url)
	print('已经是最后一页了')


def one_page(url,title):			#爬取每一个电影页面的内容，下载链接
	gsem.acquire()			#上锁
	response = requests.get('http://www.ygdy8.net{}'.format(url),headers=headers)
	response.encoding = 'gb2312'
	p = re.compile(r'(<div id="Zoom">.*?)<strong>.*?<td style="WORD-WRAP: break-word" bgcolor="#fdfddf"><a href="(.*?)">',re.S)
	reg = re.findall(p,response.text)[0]
	dy = {
		'title': title,
		'content': reg[0],
		'down_url': reg[1],
	}
	if db[MONGO_TABLE].insert(dy):		#存储到mongodb数据库
		print('--存储成功--')
	else:
		print('--存储失败--http://www.ygdy8.net{}'.format(url))

	# with open('log.txt','a') as file:
	# 	file.write(str(e)+'\n\n')
	# print(e)
	gsem.release()				#解锁


if __name__ == '__main__':
	get_dy_url(url)
