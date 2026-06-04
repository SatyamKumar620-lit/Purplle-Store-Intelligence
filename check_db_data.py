import sqlite3

conn = sqlite3.connect("store.db")

cur = conn.cursor()

cur.execute("""
SELECT
    store_id,
    COUNT(*)
FROM events
GROUP BY store_id
""")

for row in cur.fetchall():
    print(row)

conn.close()