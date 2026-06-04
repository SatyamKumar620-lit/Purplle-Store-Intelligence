import cv2
import json
import time
import uuid
import sqlite3
import sys
import os

from datetime import datetime
from ultralytics import YOLO
import supervision as sv


# ==========================
# CONFIG
# ==========================


VIDEO_NAME = sys.argv[1]

VIDEO_PATH = VIDEO_NAME

filename = os.path.basename(VIDEO_NAME)

# -----------------------------
# STORE + CAMERA DETECTION
# -----------------------------

if "Store 1" in VIDEO_NAME:

    STORE_ID = "STORE_1"

    if "CAM 1" in filename:
        CAMERA_ID = "CAM_1_ZONE"

    elif "CAM 2" in filename:
        CAMERA_ID = "CAM_2_ZONE"

    elif "CAM 3" in filename:
        CAMERA_ID = "CAM_3_ENTRY"

    elif "CAM 5" in filename:
        CAMERA_ID = "CAM_5_BILLING"

    else:
        CAMERA_ID = filename

elif "Store 2" in VIDEO_NAME:

    STORE_ID = "STORE_2"

    if "entry 1" in filename.lower():
        CAMERA_ID = "ENTRY_1"

    elif "entry 2" in filename.lower():
        CAMERA_ID = "ENTRY_2"

    elif "billing" in filename.lower():
        CAMERA_ID = "BILLING_AREA"

    elif "zone" in filename.lower():
        CAMERA_ID = "ZONE"

    else:
        CAMERA_ID = filename

else:

    STORE_ID = "UNKNOWN_STORE"
    CAMERA_ID = filename
    
EVENT_FILE = "data/events.jsonl"
DB_PATH = "store.db"

EXIT_TIMEOUT = 5  # seconds


# ==========================
# MODEL + TRACKER
# ==========================

model = YOLO("yolov8n.pt")

tracker = sv.ByteTrack()


# ==========================
# VISITOR STATE
# ==========================

visitor_state = {}

"""
visitor_state = {

    5: {
        "entry_time": 123.4,
        "last_seen": 125.2
    }

}
"""


# ==========================
# SAVE EVENT
# ==========================

def save_event(
    visitor_id,
    event_type,
    zone_id=None,
    dwell_time=None
):

    event_id = str(uuid.uuid4())

    timestamp = datetime.utcnow().isoformat()

    event = {

        "event_id": event_id,

        "visitor_id": str(visitor_id),

        "event_type": event_type,

        "camera_id": CAMERA_ID,

        "timestamp": timestamp

    }

    if dwell_time is not None:

        event["dwell_seconds"] = round(
            dwell_time,
            2
        )

    # -------------------
    # JSONL
    # -------------------

    with open(EVENT_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(event) + "\n")
        f.flush()

    # -------------------
    # SQLITE
    # -------------------

    conn = sqlite3.connect(
        DB_PATH
    )

    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO events (
            event_id,
            store_id,
            camera_id,
            visitor_id,
            event_type,
            timestamp,
            zone_id,
            dwell_ms,
            is_staff,
            confidence
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            event_id,
            STORE_ID,
            CAMERA_ID,
            str(visitor_id),
            event_type,
            timestamp,
            zone_id,
            int(dwell_time * 1000)
            if dwell_time
            else None,
            False,
            1.0
        )
    )

    conn.commit()

    conn.close()

    print(event)


# ==========================
# VIDEO
# ==========================

cap = cv2.VideoCapture(
    VIDEO_PATH
)

if not cap.isOpened():

    print("Unable to open video")

    exit()


# ==========================
# PROCESS LOOP
# ==========================

while True:

    ret, frame = cap.read()

    if not ret:
        break

    current_time = time.time()

    result = model(
        frame,
        classes=[0],
        verbose=False
    )[0]

    detections = sv.Detections.from_ultralytics(
        result
    )

    detections = tracker.update_with_detections(
        detections
    )

    annotated = frame.copy()

    if detections.tracker_id is not None:

        active_ids = set()

        for i in range(len(detections)):

            tracker_id = int(
                detections.tracker_id[i]
            )

            active_ids.add(
                tracker_id
            )

            x1, y1, x2, y2 = detections.xyxy[i]

            # ==================
            # ENTRY EVENT
            # ==================

            if tracker_id not in visitor_state:

                visitor_state[tracker_id] = {

                    "entry_time": current_time,

                    "last_seen": current_time

                }

                save_event(
                    tracker_id,
                    "ENTRY"
                )
                save_event(
                    tracker_id,
                    "ZONE_VISIT",
                    "ENTRANCE"
                )

            else:

                visitor_state[tracker_id][
                    "last_seen"
                ] = current_time

            # ==================
            # DRAW
            # ==================

            cv2.rectangle(
                annotated,
                (int(x1), int(y1)),
                (int(x2), int(y2)),
                (0, 255, 0),
                2
            )

            cv2.putText(
                annotated,
                f"ID {tracker_id}",
                (int(x1), int(y1) - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2
            )

        # ==================
        # EXIT EVENT
        # ==================

        ids_to_remove = []

        for visitor_id, data in visitor_state.items():

            if (
                current_time
                - data["last_seen"]
                > EXIT_TIMEOUT
            ):

                dwell_time = (
                    data["last_seen"]
                    - data["entry_time"]
                )

                save_event(
                    visitor_id,
                    "EXIT",
                    dwell_time
                )

                ids_to_remove.append(
                    visitor_id
                )

        for visitor_id in ids_to_remove:

            del visitor_state[
                visitor_id
            ]

    # ==================
    # STATS
    # ==================

    occupancy = len(
        visitor_state
    )

    cv2.putText(
        annotated,
        f"Occupancy: {occupancy}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 0, 255),
        2
    )

    cv2.imshow(
        "Store Intelligence",
        annotated
    )

    if cv2.waitKey(1) == 27:
        break


# ==========================
# FINAL EXITS
# ==========================

for visitor_id, data in visitor_state.items():

    dwell_time = (
        data["last_seen"]
        - data["entry_time"]
    )

    save_event(
        visitor_id,
        "EXIT",
        dwell_time=dwell_time
    )
cap.release()

cv2.destroyAllWindows()

print(
    "\nEvents saved to:",
    EVENT_FILE
)