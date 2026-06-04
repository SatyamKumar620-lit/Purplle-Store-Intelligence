import sqlite3

conn = sqlite3.connect("store.db")

cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS events (

    event_id VARCHAR PRIMARY KEY,

    store_id VARCHAR,

    camera_id VARCHAR,

    visitor_id VARCHAR,

    event_type VARCHAR,

    timestamp VARCHAR,

    zone_id VARCHAR,

    dwell_ms INTEGER,

    is_staff BOOLEAN,

    confidence FLOAT

)
""")

conn.commit()

conn.close()

print("Database created successfully")