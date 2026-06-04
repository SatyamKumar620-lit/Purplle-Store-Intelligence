import cv2
import os

VIDEO_FOLDER = "data"

for file in os.listdir(VIDEO_FOLDER):

    if file.endswith(".mp4"):

        path = os.path.join(VIDEO_FOLDER, file)

        cap = cv2.VideoCapture(path)

        cap.set(cv2.CAP_PROP_POS_FRAMES, 500)

        ret, frame = cap.read()

        if ret:

            output = f"{file}.jpg"

            cv2.imwrite(output, frame)

            print("Saved:", output)

        cap.release()