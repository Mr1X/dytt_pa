import requests
import re
import pymysql

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36'}
url = 'http://www.dytt8.net/html/gndy/dyzz/20171021/55348.html'
title = '2017年古天乐动作《杀破狼·贪狼》HD国语中字'
def one_page(url,title):			#爬取每一个电影页面的内容，下载链接
	response = requests.get(url,headers=headers)
	response.encoding = 'gbk'
	p = re.compile(r'<!--Content Start-->(.*?)<strong>.*?<td style="WORD-WRAP: break-word" bgcolor="#fdfddf"><a href="(.*?)">',re.S)
	reg = re.findall(p,response.text)[0]
	save_mysql(title,reg[0],reg[1])

def save_mysql(title,content,url):
	conn = pymysql.connect(
		host = 'localhost',
		port = 3306,
		user = 'test',
		passwd = '123456',
		db = 'movie',
		charset = 'gbk'
	)
	sql = "insert into new(title,content,url) values('{}','{}','{}')".format(title,content,url)			
	cur = conn.cursor()		#获得数据库游标
	cur.execute(sql)		#执行SQL语句
	conn.commit()			#提交到数据库
	cur.close()				#关闭游标
	conn.close()			#关闭数据库连接
	print('--存储成功--',title)

if __name__ == '__main__':	
	one_page(url,title)
	
