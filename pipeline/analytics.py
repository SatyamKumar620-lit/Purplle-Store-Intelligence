import sqlite3


def calculate_metrics():

    conn = sqlite3.connect("store.db")

    cur = conn.cursor()

    cur.execute(
        "SELECT COUNT(*) FROM events WHERE event_type='ENTRY'"
    )
    total_entries = cur.fetchone()[0]

    cur.execute(
        "SELECT COUNT(*) FROM events WHERE event_type='EXIT'"
    )
    total_exits = cur.fetchone()[0]

    cur.execute(
        "SELECT COUNT(DISTINCT visitor_id) FROM events"
    )
    unique_visitors = cur.fetchone()[0]

    cur.execute(
        """
        SELECT AVG(dwell_ms)
        FROM events
        WHERE dwell_ms IS NOT NULL
        """
    )

    avg_dwell = cur.fetchone()[0]

    if avg_dwell is None:
        avg_dwell = 0

    conn.close()

    return {
        "total_entries": total_entries,
        "total_exits": total_exits,
        "unique_visitors": unique_visitors,
        "average_dwell_seconds": round(avg_dwell / 1000, 2)
    }


if __name__ == "__main__":

    print(
        calculate_metrics()
    )