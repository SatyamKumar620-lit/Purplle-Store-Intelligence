# Design Decisions

## System Architecture

The system processes CCTV footage using YOLOv8 and ByteTrack.

Pipeline:

Video → Detection → Tracking → Event Generation → SQLite → Dashboard/API

---

# AI Assisted Decisions

## Decision 1

AI suggested YOLOv8n.

Accepted because:
- Fast
- Lightweight
- Good enough accuracy

---

## Decision 2

AI suggested SQLite.

Accepted because:
- Easy deployment
- No external dependency

---

## Decision 3

AI suggested ByteTrack.

Accepted because:
- Stable tracking IDs
- Easy integration with YOLO