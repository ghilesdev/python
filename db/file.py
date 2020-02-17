import pymysql

db = pymysql.connect("localhost", "root", "", "users")
cursor = db.cursor()
"""
    cursor.execute("SELECT VERSION()")
    data=cursor.fetchone()
    print((data))
"""


# creating a new sql query
sql = """ CREATE TABLE UserTable(
    name CHAR(20) NOT NULL,
     age INTEGER, 
     job CHAR(100))"""


'''
#inserting a row into the table
sql="""INSERT INTO TestTable(
name, location, gender, age)
VALUES ("mike", "US", "M", 30)
"""

try:
    #executing the query
    cursor.execute(sql)
    db.commit()
except:
    db.rollback()
'''

# update a value in the table
# sql2 = "UPDATE TestTable SET age = 30 WHERE name = 'aghiles'"

try:
    cursor.execute(sql)
    db.commit()
except:
    db.rollback()

# reading from table
sql = """SELECT * FROM TestTable"""
try:
    cursor.execute(sql)
    result = cursor.fetchall()
    for row in result:
        name = row[0]
        location = row[1]
        gender = row[2]
        age = row[3]
        print(f"name: {name}, location: {location}, gender: {gender}, age: {age}")
except:
    print("unable to fetch data")

# sql_delete = "DELETE FROM TestTable WHERE name = 'james'"
# try:
#     cursor.execute(sql_delete)
#     db.commit()
# except:
#     db.rollback()

# closing the database
db.close()
