import os
import sys
import django
import cv2



BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from analytics.models import Detection
from ultralytics import YOLO
from drones.models import Drone
from alerts.models import Alert



INTERESTED_OBJECTS = [
    "person", "car", "truck", "bus", "motorcycle", "bicycle",
    "bird", "dog", "cat"
]


OBJECT_PRIORITY = {
    "person": 5,
    "car": 4,
    "truck": 5,
    "bus": 5,
    "motorcycle": 4,
    "bicycle": 3,
    "dog": 3,
    "cat": 2,
    "bird": 2,
}


def calculate_risk_score(class_name, confidence, x1, y1, x2, y2, frame_width, frame_height):
    box_area = (x2 - x1) * (y2 - y1)
    frame_area = frame_width * frame_height
    size_ratio = box_area / frame_area

    object_center_x = (x1 + x2) / 2
    object_center_y = (y1 + y2) / 2

    frame_center_x = frame_width / 2
    frame_center_y = frame_height / 2

    center_distance_x = abs(object_center_x - frame_center_x) / frame_width
    center_distance_y = abs(object_center_y - frame_center_y) / frame_height

    center_score = 1 - ((center_distance_x + center_distance_y) / 2)

    priority = OBJECT_PRIORITY.get(class_name, 1)

    risk_score = (
        priority * 30 +
        confidence * 30 +
        size_ratio * 100 +
        center_score * 40
    )

    return risk_score


def get_risk_level(score):
    if score >= 170:
        return "CRITICAL"
    elif score >= 130:
        return "HIGH"
    elif score >= 90:
        return "MEDIUM"
    return "LOW"


def detect_collision_risk_yolo(video_path, drone_id=1, max_frames=10):
    drone = Drone.objects.get(id=drone_id)
    model = YOLO("yolov8n.pt")

    cap = cv2.VideoCapture(video_path)
    os.makedirs("analytics/detected_frames", exist_ok=True)

    risky_frames = []
    frame_count = 0

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        frame_count += 1
        frame_height, frame_width = frame.shape[:2]

        results = model(frame, verbose=False)

        frame_risk_score = 0
        detected_labels = []

        for result in results:
            for box in result.boxes:
                class_id = int(box.cls[0])
                confidence = float(box.conf[0])
                class_name = model.names[class_id]
                
                if class_name not in INTERESTED_OBJECTS:
                    continue

                if confidence < 0.35:
                    continue

                x1, y1, x2, y2 = map(int, box.xyxy[0])

                risk_score = calculate_risk_score(
                    class_name,
                    confidence,
                    x1, y1, x2, y2,
                    frame_width,
                    frame_height
                )

                risk_level = get_risk_level(risk_score)
                detected_labels.append({
                    "class_name": class_name,
                    "confidence": confidence,
                    "risk_level": risk_level
                })
                frame_risk_score += risk_score
                

                label = f"{class_name.upper()} {confidence:.2f} | {risk_level}"

                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                cv2.putText(
                    frame,
                    label,
                    (x1, max(y1 - 10, 20)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 0, 255),
                    2
                )

        if frame_risk_score > 0:
            risky_frames.append(
                (frame_risk_score, frame_count, frame.copy(), detected_labels)
            )

    cap.release()

    risky_frames.sort(reverse=True, key=lambda x: x[0])
    top_frames = risky_frames[:max_frames]

    for index, (score, frame_number, frame, labels) in enumerate(top_frames, start=1):
        output_path = f"analytics/detected_frames/yolo_risk_{index}_frame_{frame_number}.jpg"
        cv2.imwrite(output_path, frame)
        for item in labels:
          Detection.objects.create(
             drone=drone,
             object_type=item["class_name"].upper(),
             confidence=float(item["confidence"]),
             risk_level=item["risk_level"],
             image_path=output_path
            )

    if top_frames:
        all_objects = []
        for _, _, _, labels in top_frames:
           for item in labels:
               all_objects.append(item["class_name"])

        unique_objects = list(set(all_objects))

        Alert.objects.create(
            drone=drone,
            alert_type="OBSTACLE_DETECTED",
            severity="CRITICAL",
            message=(
                f"High collision-risk objects detected: {', '.join(unique_objects)}. "
                f"{len(top_frames)} highest-risk frames saved."
            )
        )
    print(f"YOLO risk detection completed. Saved {len(top_frames)} highest-risk frames.")
    
if __name__ == "__main__":
    detect_collision_risk_yolo(
        "analytics/video_samples/sample.mp4",
        drone_id=1,
        max_frames=10
    )