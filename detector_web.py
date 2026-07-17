# ===================================
# library ต่างๆในการใช้ในโค้ด
# ===================================
from ultralytics import YOLO
import cv2
import torch
import time
import csv
import os
from datetime import datetime

# ===================================
# เมนูการเลือก CPU หรือ GPU ในการรันโค้ด
# ===================================

# ===================================
# เลือก GPU อัตโนมัติ
# ===================================
if torch.cuda.is_available():
    device = 0
    device_name = torch.cuda.get_device_name(0)
    print(f"Using GPU : {device_name}")
else:
    device = "cpu"
    device_name = "CPU"
    print("Using CPU")
# ===================================
# เมนูการเลือกบันทึกข้อมูล
# ===================================
SAVE_CSV = True
print("CSV Logging : ON")
model = YOLO("best1.pt")
model.to(device)

# ===================================
# สร้างชื่อไฟล์ CSV. : วัน/เดือน/ปี__ชั่วโมง/นาที
# ===================================
os.makedirs("Data", exist_ok=True)
today = datetime.now()
csv_file = os.path.join(
    "Data",
    f"result_{today.strftime('%d_%m_%Y__%H_%M')}.csv"   # การตั้งค่าชื่อไฟล์
)

if SAVE_CSV:    # ค่าต่างๆ ตารางExcel  

    if not os.path.exists(csv_file):

        with open(csv_file, "w", newline="", encoding="utf-8") as f:

            writer = csv.writer(f)

            writer.writerow([
                "Date",
                "Time",
                "Device",
                "FPS",
                "Tracking ID",
                "Confidence (%)",
                "Count"
            ])

    print(f"\nCSV File : {csv_file}")

# =====================================
# เปิดกล้อง
# =====================================
cap = cv2.VideoCapture(1)

if not cap.isOpened():
    print("Cannot open camera")
    exit()

# ใช้ MJPG เพื่อเพิ่ม FPS ของเว็บแคม (ถ้ารองรับ)
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))

# ตั้งค่ากล้อง
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 640)
cap.set(cv2.CAP_PROP_FPS, 60)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

# ตรวจสอบค่าที่กล้องใช้งานจริง
print("Width :", cap.get(cv2.CAP_PROP_FRAME_WIDTH))
print("Height:", cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
print("FPS   :", cap.get(cv2.CAP_PROP_FPS))

# ===================================
# Line Crossing + Object Tracking 
# ===================================
LINE_Y = 320

count = 0
detected = 0
fps = 0.0
confidence = 0.0

dashboard_data = {
    "count": 0,
    "total": 0,
    "confidence": 0.0,
    "fps": 0.0,
    "status": "ONLINE",
    "device": device_name,
    "model":"best1.pt",
    "tracker":"ByteTrack"
}

track_history = {}
track_last_seen = {}

counted_ids = set()

prev = time.time()

def generate_frames():

    global count
    global fps
    global detected
    global prev
    global confidence
    global dashboard_data
    global last_frame

    while True:

        ret, frame = cap.read()

        if not ret:
            break
        
        last_frame = frame.copy()

        results = model.track(
            frame,
            persist=True,
            tracker="bytetrack.yaml",
            imgsz=640,
            conf=0.50,
            device=device,
            verbose=False
        )

        detected = 0

        if results and results[0].boxes is not None:

            boxes = results[0].boxes
            detected = len(boxes)

            for box in boxes:

                x1, y1, x2, y2 = map(int, box.xyxy[0])
                confidence = round(float(box.conf) * 100, 1)
                track_id = int(box.id) if box.id is not None else -1

                cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 2)

                text = f"ID:{track_id} {confidence:.1f}%"

                cv2.rectangle(frame, (x1, max(0,y1-22)), (x1+120, y1), (0,0,0), -1)

                cv2.putText(
                    frame,
                    text,
                    (x1+3, max(15,y1-5)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.45,
                    (0,255,0),
                    1
                )

                cx = (x1 + x2) // 2
                cy = y2
                print(track_id, track_history.get(track_id), cy)

                cv2.circle(frame, (cx,cy), 4, (0,0,255), -1)

                if track_id != -1:

                    if track_id in track_history:

                        # วัตถุผ่านเส้นจากบนลงล่าง
                        if track_history[track_id] < LINE_Y <= cy:

                            if track_id not in counted_ids:

                                counted_ids.add(track_id)

                                count += 1

                                print("COUNT =", count)

                                if SAVE_CSV:

                                    now = datetime.now()

                                    with open(csv_file, "a", newline="", encoding="utf-8") as f:

                                        csv.writer(f).writerow([
                                            now.strftime("%Y-%m-%d"),
                                            now.strftime("%H:%M:%S"),
                                            device_name,
                                            round(fps, 1),
                                            track_id,
                                            round(confidence, 1),
                                            count
                                        ])

                    # อัปเดตตำแหน่งล่าสุดของ ID
                    track_history[track_id] = cy
                    track_last_seen[track_id] = time.time()

        cv2.line(frame,(0,LINE_Y),(640,LINE_Y),(0,0,255),3)

        now = time.time()

        fps = 1/(now-prev)

        prev = now 
        dashboard_data["count"] = detected
        dashboard_data["total"] = count
        dashboard_data["confidence"] = round(confidence, 1)
        dashboard_data["fps"] = round(fps, 1)
        dashboard_data["status"] = "ONLINE"

# ==========================
# Clear old Track IDs
# ==========================

    current_time = time.time()

    expired_ids = [
        tid for tid, t in track_last_seen.items()
        if current_time - t > 3
]

    for tid in expired_ids:

        track_last_seen.pop(tid, None)
        track_history.pop(tid, None)
        counted_ids.discard(tid)

        cv2.putText(frame,f"FPS : {fps:.1f}",(20,35),0,0.75,(0,0,255),2)
        cv2.putText(frame,f"Detected : {detected}",(20,70),0,0.75,(255,255,0),2)
        cv2.putText(frame,f"Count : {count}",(20,105),0,0.75,(0,255,255),2)

        _, buffer = cv2.imencode(".jpg", frame)

        frame = buffer.tobytes()

        yield (
            b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' +
            frame +
            b'\r\n'
        )

# ==========================
# Capture Image
# ==========================

last_frame = None

def capture_image():

    global last_frame

    if last_frame is None:
        return False

    os.makedirs("Capture", exist_ok=True)

    filename = datetime.now().strftime(
        "Capture/capture_%Y%m%d_%H%M%S.jpg"
    )

    cv2.imwrite(filename, last_frame)

    print(f"Saved : {filename}")

    return filename

# ==========================
# ส่งข้อมูลให้ Dashboard
# ==========================
def get_status():

    history = []
    total = 0

    if os.path.exists(csv_file):

        with open(csv_file, "r", encoding="utf-8") as f:

            reader = list(csv.DictReader(f))

            if len(reader) > 0:
                total = int(reader[-1]["Count"])   # อ่าน Count ล่าสุด

            for row in reader[-10:][::-1]:

                history.append({

                    "time": row["Time"],
                    "count": row["Count"]

                })

    dashboard_data["total"] = total
    dashboard_data["history"] = history

    return dashboard_data

# ==========================
# End
# ==========================