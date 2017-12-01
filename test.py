# import pymysql
# conn = pymysql.connect(
# 		host = 'localhost',
# 		port = 3306,
# 		user = 'test',
# 		passwd = '123456',
# 		db = 'movie'
# 	)
# cur = conn.cursor()
# sql = "insert into new(title) values('python')"
# try:
# 	cur.execute(sql)
# 	conn.commit()
# 	print('插入成功')
# except:
# 	print('插入失败')
# conn.close()

# import pymysql
# import datetime
# import time
# import threading
# def insert(io):
# 	while True:
# 		time_now = time.strftime("%H:%M:%S")
# 		print(io,time_now)
# 		conn = pymysql.connect(user = "test", passwd = "123456", host = "localhost", db = "test", port = 3306)
# 		#这里连接数据库要写在里面，不然多线程的时候回出现死锁情况
# 		cur = conn.cursor()
# 		sql = "insert into test({}) values('{}')".format(io,io)
# 		print(sql)
# 		cur.execute(sql)
# 		conn.commit()
# 		cur.close()
# 		conn.close()
# 		time.sleep(5)

# if __name__ == "__main__":
#     #这里进出的参数不能用in,out,不然SQL语法有问题
#     threading.Thread(target=insert,args=('jin',)).start()		
#     threading.Thread(target=insert,args=('chu',)).start()

try:
	f = open('1.txt')
	for line in f:
		print(line)
	f.close()
except Exception as e:
	with open('log.txt','a') as file:
		file.write(str(e)+'\n')
