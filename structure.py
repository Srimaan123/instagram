import sqlite3

def init_db():
	with sqlite3.connect("data.db") as conn:
		cursor = conn.cursor()
		cursor.execute("""
			create table if not exists users(
				id integer primary key autoincrement,
				username text,
				password text,
				mobile_number text,
				is_private text,
				last_seen text
			)
		""")

		cursor.execute("""
		create table if not exists requests(
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			requested_by text,
			requested_to text,
			is_accepted text,
			is_rejected text,
			is_seen text) 
		""")

		cursor.execute("""
		create table if not exists chats(
		id TEXT,
		message TEXT,
		sender TEXT,
		receiver TEXT,
		is_seen TEXT,
		is_deleted TEXT
		)
		""")

		conn.commit()