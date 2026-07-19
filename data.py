import sqlite3 
conn = sqlite3.connect("data.db")
cursor = conn.cursor()

cursor.execute("insert into users(username,password,is_private) values('Srimaan123','Srimaan123','True')")

conn.commit()
conn.close()
print("completed")