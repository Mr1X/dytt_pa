import requests
import re
import pymysql
import threading
#
#电影天堂的32页存在问题，所以多线程爬到32页就会挂掉
#
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36'}
url = 'http://www.ygdy8.net/html/gndy/dyzz/index.html'

gsem = threading.Semaphore(10)		#设置信号量为5，多线程做多5个

def get_dy_url(url):
	response = requests.get(url,headers=headers)
	response.encoding = 'gbk'							#这里原网站是gb2312的编码，但是有些字符不能编码，所以换成gbk
	p = r'<a href="(.*?)" class="ulink">(.*?)</a>'
	reg = re.findall(p,response.text)
	for dy_url,title in reg:				#每一个电影页面开启多线程
		threading.Thread(target=one_page,args=(dy_url,title,)).start()
		# one_page(dy_url,title)

	p = r"<a href='(.*?)'>下一页</a>"		#如果有下一页则递归爬取下一页
	reg = re.findall(p,response.text)
	if reg:
		next_url = 'http://www.ygdy8.net/html/gndy/dyzz/' + reg[0]
		print('正在爬取'+next_url)
		get_dy_url(next_url)
	# print('已经是最后一页了')

def one_page(url,title):			#爬取每一个电影页面的内容，下载链接
	gsem.acquire()			#上锁
	response = requests.get('http://www.ygdy8.net{}'.format(url),headers=headers)
	response.encoding = 'gbk'
	p = re.compile(r'<!--Content Start-->(.*?)<strong>.*?<td style="WORD-WRAP: break-word" bgcolor="#fdfddf"><a href="(.*?)">',re.S)
	reg = re.findall(p,response.text)[0]
	save_mysql(title,reg[0],reg[1])				#存储到MySQL数据库
	print('--存储成功--',title)
	gsem.release()			#解锁

	# except Exception as e:
	# 	with open('log.txt','a') as file:		#将错误日志写入到日志文件
	# 		file.write(str(e)+'\n\n')
	# 	print('--存储失败--',e,dy['title'])
	# # except Exception as e:
	# 	with open('log.txt','a') as file:
	# 		file.write(str(e)+'\n\n')
	# 	print(e)

def save_mysql(title,content,url):
	conn = pymysql.connect(
		host = 'localhost',
		port = 3306,
		user = 'test',
		passwd = '123456',
		db = 'movie',
		charset = 'gbk'
	)
	sql = "insert into new(title,content,url) values('{}','{}','{}')".format(title,content.replace("'","’"),url)			
	cur = conn.cursor()		#获得数据库游标
	cur.execute(sql)		#执行SQL语句
	conn.commit()			#提交到数据库
	cur.close()				#关闭游标
	conn.close()			#关闭数据库连接

if __name__ == '__main__':	
	get_dy_url(url)
	print('爬取结束')
	
