from ultralytics import YOLO
import supervision as sv
import cv2

model = YOLO("yolov8n.pt")

tracker = sv.ByteTrack()

cap = cv2.VideoCapture(r"data/CAM 1.mp4")

while True:

    ret, frame = cap.read()

    if not ret:
        break

    result = model(frame)[0]

    detections = sv.Detections.from_ultralytics(
        result
    )

    detections = tracker.update_with_detections(
        detections
    )

    annotated = frame.copy()

    for i in range(len(detections)):

        if detections.tracker_id is None:
            continue

        tracker_id = detections.tracker_id[i]

        x1, y1, x2, y2 = detections.xyxy[i]

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
            0.6,
            (0, 255, 0),
            2
        )

    cv2.imshow("Tracking", annotated)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()