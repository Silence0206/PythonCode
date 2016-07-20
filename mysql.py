# -*- coding: utf-8 -*-
import mysql.connector

conn = mysql.connector.connect(user='root', password='58424716', database='python_learn')
cursor = conn.cursor()

# cursor.execute('create table user (id varchar(20) primary key, name varchar(20))')
#cursor.execute('insert into user (id, name) values (%s, %s)', ['3', '我们'])
# print(cursor.rowcount)
cursor.execute('select * from user where id = %s', ('1',))
values = cursor.fetchall()
print(values)
# conn.commit()
cursor.close()
conn.close()
#用于学习