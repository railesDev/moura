import sqlite3

conn = sqlite3.connect('users.db')
c = conn.cursor()
c.execute(f'DELETE FROM users')
c.execute(f'DELETE FROM reactions')
conn.commit()
conn.close()
