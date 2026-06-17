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


def detect_motion(video_path, drone_id=1, max_frames=10):
    drone = Drone.objects.get(id=drone_id)

    cap = cv2.VideoCapture(video_path)
    first_frame = None
    frame_count = 0
    motion_frames = []

    os.makedirs("analytics/detected_frames", exist_ok=True)

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        frame_count += 1

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        if first_frame is None:
            first_frame = gray
            continue

        frame_delta = cv2.absdiff(first_frame, gray)
        thresh = cv2.threshold(frame_delta, 30, 255, cv2.THRESH_BINARY)[1]

        contours, _ = cv2.findContours(
            thresh.copy(),
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        motion_score = 0

        for contour in contours:
            area = cv2.contourArea(contour)

            if area < 500:
                continue

            motion_score += area

            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        if motion_score > 0:
            motion_frames.append((motion_score, frame_count, frame.copy()))

    cap.release()

    motion_frames.sort(reverse=True, key=lambda x: x[0])
    top_frames = motion_frames[:max_frames]

    for index, (score, frame_number, frame) in enumerate(top_frames, start=1):
        output_path = f"analytics/detected_frames/high_motion_{index}_frame_{frame_number}.jpg"
        cv2.imwrite(output_path, frame)

    if top_frames:
        Alert.objects.create(
            drone=drone,
            alert_type="OBSTACLE_DETECTED",
            severity="CRITICAL",
            message=f"Suspicious activity detected. {len(top_frames)} high-motion frames captured for review."
        )

    print(f"Video detection completed. Saved {len(top_frames)} high-motion frames.")

if __name__ == "__main__":
    detect_motion("analytics/video_samples/sample.mp4", drone_id=1)