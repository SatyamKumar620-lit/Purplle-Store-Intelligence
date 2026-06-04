import sqlite3

conn = sqlite3.connect("store.db")
cur = conn.cursor()

cur.execute("""
SELECT
    store_id,
    camera_id,
    COUNT(*) as total_events
FROM events
GROUP BY store_id, camera_id
ORDER BY store_id, camera_id
""")

rows = cur.fetchall()

print("\n===== CAMERA EVENT SUMMARY =====\n")

for row in rows:
    print(row)

conn.close()