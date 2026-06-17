import cv2
import os
import sys
import django

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from drones.models import Drone
from alerts.models import Alert


def detect_human(video_path, drone_id=1, max_frames=10):
    drone = Drone.objects.get(id=drone_id)

    cap = cv2.VideoCapture(video_path)

    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

    os.makedirs("analytics/detected_frames", exist_ok=True)

    detected_frames = []
    frame_count = 0

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        frame_count += 1

        resized_frame = cv2.resize(frame, (640, 360))

        boxes, weights = hog.detectMultiScale(
                           resized_frame,
                           winStride=(4,4),
                           padding=(8,8),
                           scale=1.05
                       )
        from imutils.object_detection import non_max_suppression
        import numpy as np
        rects = np.array(
                          [[x, y, x+w, y+h] for (x, y, w, h) in boxes]
                          )
        pick = non_max_suppression(rects, probs=None, overlapThresh=0.65)
        if len(boxes) > 0:
            for (xA, yA, xB, yB) in pick:
                width = xB - xA
                height = yB - yA
                if width < 40:
                    continue
                if height < 80:
                    continue
                cv2.rectangle(resized_frame,
                              (xA, yA),
                              (xB, yB),
                              (0,0,255),2
                              )
                detected_frames.append((frame_count, resized_frame.copy()))

        if len(detected_frames) >= max_frames:
            break

    cap.release()

    for index, (frame_number, frame) in enumerate(detected_frames, start=1):
        output_path = f"analytics/detected_frames/human_detected_{index}_frame_{frame_number}.jpg"
        cv2.imwrite(output_path, frame)

    if detected_frames:
        Alert.objects.create(
            drone=drone,
            alert_type="OBSTACLE_DETECTED",
            severity="CRITICAL",
            message=f"Potential intruder detected. {len(detected_frames)} evidence frames saved."
        )

    print(f"Human detection completed. Saved {len(detected_frames)} frames.")


if __name__ == "__main__":
    detect_human("analytics/video_samples/sample.mp4", drone_id=1)