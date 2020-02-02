import pymysql

db = pymysql.connect("localhost", 'root', "", "users")
cursor=db.cursor()
'''
    cursor.execute("SELECT VERSION()")
    data=cursor.fetchone()
    print((data))
'''


#creating a new sql query
sql=""" CREATE TABLE TestTable(
    name CHAR(20) NOT NULL,
     location CHAR(100),
     gender CHAR(1),
     age INTEGER)"""

#executing the query
cursor.execute(sql)

#closing the database
db.close()