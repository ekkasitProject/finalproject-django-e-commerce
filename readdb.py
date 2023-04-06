
import sqlite3

conn = sqlite3.connect('db.sqlite3')
c = conn.cursor()


with conn:
	c.execute("""SELECT * FROM myapp_allproduct""")
	# data = c.fetchall()
	data =c.fetchmany(5)
	print(data)