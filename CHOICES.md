# Technology Choices

## Model Selection

YOLOv8n

Reason:
- Fast inference
- Good balance between speed and accuracy

---

## Tracking

ByteTrack

Reason:
- Reliable object association
- Works well with retail CCTV

---

## Event Schema

event_id
visitor_id
camera_id
store_id
event_type
timestamp
dwell_ms

Reason:
Supports analytics and reporting.

---

## Database

SQLite

Reason:
Simple deployment for challenge environment.