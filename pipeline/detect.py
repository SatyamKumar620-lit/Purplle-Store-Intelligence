from ultralytics import YOLO

model = YOLO("yolov8n.pt")

def detect(frame):

    results = model(frame)

    detections = []

    for box in results[0].boxes:

        cls = int(box.cls[0])

        if cls == 0:

            detections.append(box)

    return detections
