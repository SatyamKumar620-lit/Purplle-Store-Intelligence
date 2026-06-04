import cv2

cap = cv2.VideoCapture(
    "data/videos/store.mp4"
)

while True:

    ret,frame = cap.read()

    if not ret:
        break

    detections = detect(frame)

    tracks = update_tracks(detections)

    # Generate events

cap.release()