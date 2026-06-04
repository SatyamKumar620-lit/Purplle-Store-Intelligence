import streamlit as st
import sqlite3
import pandas as pd
import sys
import os

# Import analytics.py
sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

from pipeline.analytics import calculate_metrics

# --------------------------------
# PAGE SETTINGS
# --------------------------------

st.set_page_config(
    page_title="Purplle Store Intelligence",
    page_icon="🛍️",
    layout="wide"
)

# --------------------------------
# DATABASE
# --------------------------------

conn = sqlite3.connect("store.db")

# --------------------------------
# METRICS
# --------------------------------

metrics = calculate_metrics()

# --------------------------------
# TITLE
# --------------------------------

st.title("🛍️ Purplle Store Intelligence Dashboard")

st.write(
    "AI-powered retail analytics using CCTV footage and visitor tracking."
)

# --------------------------------
# KPI CARDS
# --------------------------------

billing_visitors = pd.read_sql(
    """
    SELECT COUNT(DISTINCT visitor_id)
    FROM events
    WHERE camera_id LIKE '%BILLING%'
    """,
    conn
).iloc[0,0]

conversion_rate = 0

if metrics["unique_visitors"] > 0:
    conversion_rate = round(
        billing_visitors /
        metrics["unique_visitors"] * 100,
        2
    )

camera_count = pd.read_sql(
    """
    SELECT COUNT(DISTINCT camera_id)
    FROM events
    """,
    conn
).iloc[0, 0]


c1, c2, c3, c4, c5, c6 = st.columns(6)

with c1:
    st.metric(
        "👥 Visitors",
        metrics["unique_visitors"]
    )

with c2:
    st.metric(
        "🚪 Entries",
        metrics["total_entries"]
    )

with c3:
    st.metric(
        "🚶 Exits",
        metrics["total_exits"]
    )

with c4:
    st.metric(
        "⏱ Avg Dwell",
        f"{metrics['average_dwell_seconds']} sec"
    )

with c5:
    st.metric(
        "📷 Cameras",
        camera_count
    )

with c6:
    st.metric(
        "💰 Conversion",
        f"{conversion_rate}%"
    )

# -----------------------------
# STORE LAYOUTS
# -----------------------------

st.divider()

st.subheader("🏬 Store Layouts")

col1, col2 = st.columns(2)

with col1:
    st.image(
        "data/Store 1/Store 1 - layout.png",
        caption="Store 1 Layout"
    )

with col2:
    st.image(
        "data/Store 2/store 2 - layout.png",
        caption="Store 2 Layout"
    )
    
    
# -----------------------------
# STORE COMPARISON
# -----------------------------

st.divider()

st.subheader("🏪 Store Comparison")

store_df = pd.read_sql(
    """
    SELECT
        store_id,
        COUNT(*) as total_events
    FROM events
    GROUP BY store_id
    """,
    conn
)

if not store_df.empty:

    st.bar_chart(
        store_df.set_index("store_id")
    )

    st.dataframe(
        store_df,
        use_container_width=True
    )
    
    
# -----------------------------
# STORE PERFORMANCE LEADERBOARD
# -----------------------------

st.header("🏆 Store Performance Leaderboard")

leaderboard = pd.read_sql(
    """
    SELECT
        store_id,
        COUNT(*) as total_events
    FROM events
    GROUP BY store_id
    ORDER BY total_events DESC
    """,
    conn
)

st.dataframe(
    leaderboard,
    use_container_width=True
) 

# -----------------------------
# BILLING AREA FUNNEL
# -----------------------------

st.header("💰 Visitor Conversion Funnel")

funnel_df = pd.DataFrame({
    "Stage": [
        "Visitors",
        "Billing Area"
    ],
    "Count": [
        metrics["unique_visitors"],
        billing_visitors
    ]
})

st.bar_chart(
    funnel_df.set_index("Stage")
)  

# -----------------------------
# STORE WISE TRAFFIC
# -----------------------------

st.header("📈 Store Wise Traffic")

traffic_store = pd.read_sql(
    """
    SELECT
        store_id,
        COUNT(DISTINCT visitor_id) as visitors
    FROM events
    GROUP BY store_id
    """,
    conn
)

st.bar_chart(
    traffic_store.set_index("store_id")
)

st.dataframe(
    traffic_store,
    use_container_width=True
)

# --------------------------------
# CAMERA WISE EVENTS
# --------------------------------

st.header("📷 Camera Analytics")

camera_df = pd.read_sql(
    """
    SELECT
        camera_id,
        COUNT(*) as total_events
    FROM events
    GROUP BY camera_id
    ORDER BY total_events DESC
    """,
    conn
)

if not camera_df.empty:
    st.bar_chart(
        camera_df.set_index("camera_id")
    )

    st.dataframe(
        camera_df,
        use_container_width=True
    )

# --------------------------------
# EVENT TYPES
# --------------------------------

st.header("📊 Event Distribution")

event_df = pd.read_sql(
    """
    SELECT
        event_type,
        COUNT(*) as total
    FROM events
    GROUP BY event_type
    """,
    conn
)

if not event_df.empty:
    st.bar_chart(
        event_df.set_index("event_type")
    )

# --------------------------------
# ZONE ANALYTICS
# --------------------------------

st.header("🔥 Zone Analytics")

zone_df = pd.read_sql(
    """
    SELECT
        zone_id,
        COUNT(*) as visits
    FROM events
    WHERE zone_id IS NOT NULL
    GROUP BY zone_id
    """,
    conn
)

if not zone_df.empty:
    st.bar_chart(
        zone_df.set_index("zone_id")
    )

    st.dataframe(
        zone_df,
        use_container_width=True
    )

# --------------------------------
# TRAFFIC BY HOUR
# --------------------------------

st.header("🕒 Peak Traffic")

traffic_df = pd.read_sql(
    """
    SELECT
        substr(timestamp,12,2) as hour,
        COUNT(*) as total
    FROM events
    GROUP BY hour
    ORDER BY hour
    """,
    conn
)

if not traffic_df.empty:
    st.line_chart(
        traffic_df.set_index("hour")
    )

# --------------------------------
# LATEST EVENTS
# --------------------------------

st.header("📄 Latest Events")

latest_df = pd.read_sql(
    """
    SELECT *
    FROM events
    ORDER BY timestamp DESC
    LIMIT 50
    """,
    conn
)

st.dataframe(
    latest_df,
    use_container_width=True
)

# --------------------------------
# AI INSIGHTS
# --------------------------------

st.header("🤖 AI Business Insights")

top_store = pd.read_sql(
    """
    SELECT
        store_id,
        COUNT(*) as total
    FROM events
    GROUP BY store_id
    ORDER BY total DESC
    LIMIT 1
    """,
    conn
)

if not top_store.empty:

    top_store_name = top_store.iloc[0]["store_id"]

    st.success(
        f"Highest activity observed in {top_store_name}"
    )

st.info(
    f"Conversion Rate: {conversion_rate}%"
)

if metrics["average_dwell_seconds"] > 15:
    st.success(
        "Customer engagement is healthy."
    )
else:
    st.warning(
        "Customer engagement is low."
    )

# --------------------------------
# REFRESH
# --------------------------------

if st.button("Refresh Dashboard"):
    st.rerun()

# --------------------------------
# CLOSE DB
# --------------------------------

conn.close()