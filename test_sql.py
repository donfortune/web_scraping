import sqlite3
#connect to sql db
connection = sqlite3.connect("data.db")
cursor = connection.cursor()

#query all data
cursor.execute("SELECT * FROM events WHERE band='lions'")
print(cursor.fetchall())

#insert new rows
new_rows = [('cats', 'cats city', '2088.10.10'),

        ('monkey', 'monkey city', '2088.10.10')]

cursor.executemany("INSERT INTO events VALUES(?,?,?)", new_rows)
connection.commit() #write new changes to db



