import sqlite3

conn = sqlite3.connect("store.db")

cur = conn.cursor()

cur.execute("""
SELECT
visitor_id,
zone_id,
timestamp
FROM events
WHERE zone_id IS NOT NULL
ORDER BY visitor_id,timestamp
""")

rows = cur.fetchall()

for row in rows:

    print(row)

conn.close()