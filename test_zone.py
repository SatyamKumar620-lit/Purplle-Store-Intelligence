import cv2
from ultralytics import YOLO

model = YOLO("yolov8n.pt")

video = "data/Store 2/zone.mp4"

cap = cv2.VideoCapture(video)

frame_count = 0
total_people = 0

while True:

    ret, frame = cap.read()

    if not ret:
        break

    frame_count += 1

    # check every 30th frame
    if frame_count % 30 != 0:
        continue

    results = model(
        frame,
        classes=[0],
        verbose=False
    )

    count = len(results[0].boxes)

    if count > 0:
        print(
            f"Frame {frame_count}: {count} people detected"
        )

        total_people += count

cap.release()

print("\nTotal detections:", total_people)