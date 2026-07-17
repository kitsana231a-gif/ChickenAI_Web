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

print("=" * 35)
print("Egg Tracking")
print("=" * 35)
print("1) GPU")
print("2) CPU")
print("=" * 35)
choice = input("Select Device (1/2): ")

if choice == "1" and torch.cuda.is_available():
    device = 0
    device_name = torch.cuda.get_device_name(0)
    print(f"\nUsing GPU : {device_name}")
else:
    device = "cpu"
    device_name = "CPU"
    print("\nUsing CPU")

# ===================================
# เมนูการเลือกบันทึกข้อมูล
# ===================================
print("\n" + "=" * 35)
print("      Save Counting Data")
print("=" * 35)
print("1) Save CSV.")
print("2) Don't Save")
print("=" * 35)

save_choice = input("Select (1/2): ")

SAVE_CSV = (save_choice == "1")

if SAVE_CSV:
    print("\nCSV Logging : ON")
else:
    print("\nCSV Logging : OFF")

model = YOLO("best_1.pt")
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
cap = cv2.VideoCapture(0)

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
track_history = {}
counted_ids = set()
prev = time.time()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model.track(
        frame,
        persist=True,
        tracker="bytetrack.yaml",
        imgsz=640,
        conf=0.50,      # ปรับ confiden ไม่ควรเกิน 0.50 - 0.60
        device=device,
        verbose=False
    )

    detected = 0

    if results and results[0].boxes is not None:
        boxes = results[0].boxes
        detected = len(boxes)

        for box in boxes:
            x1,y1,x2,y2 = map(int, box.xyxy[0])
            confidence = float(box.conf)
            track_id = int(box.id) if box.id is not None else -1

            cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2)    # เปลี่ยนสีกรอบ

            text=f"ID:{track_id} {confidence*100:.1f}%"
            cv2.rectangle(frame,(x1,max(0,y1-22)),(x1+120,y1),(0,0,0),-1)
            cv2.putText(frame,text,(x1+3,max(15,y1-5)),
                        cv2.FONT_HERSHEY_SIMPLEX,0.45,(0,255,0),1)

            cx=(x1+x2)//2
            cy=y1+5
            cv2.circle(frame,(cx,cy),4,(0,0,255),-1)

            if track_id!=-1:
                if track_id in track_history:
                    if track_history[track_id] < LINE_Y <= cy:
                        if track_id not in counted_ids:
                            counted_ids.add(track_id)
                            count += 1
                            if SAVE_CSV:
                                now = datetime.now()
                                current_fps = 1/(time.time()-prev) if time.time()!=prev else 0
                                with open(csv_file,"a",newline="",encoding="utf-8") as f:
                                    csv.writer(f).writerow([
                                        now.strftime("%Y-%m-%d"),
                                        now.strftime("%H:%M:%S"),
                                        device_name,
                                        round(current_fps,1),
                                        track_id,
                                        round(confidence*100,2),
                                        count
                                    ])
                track_history[track_id]=cy

    cv2.line(frame,(0,LINE_Y),(640,LINE_Y),(0,0,255),3)

    now=time.time()
    fps=1/(now-prev)
    prev=now

# ===================================
# เมนู UI ข้างๆจอ
# ===================================
    cv2.putText(frame,f"FPS : {fps:.1f}",(20,35),0,0.75,(0,0,255),2)
    cv2.putText(frame,f"Detected : {detected}",(20,70),0,0.75,(255,255,0),2)
    cv2.putText(frame,f"Count : {count}",(20,105),0,0.75,(0,255,255),2)
    cv2.putText(frame,"R : Reset Count",(20,140),0,0.55,(255,0,255),2)
    cv2.putText(frame,"Q : Quit",(20,165),0,0.55,(255,0,255),2)
    cv2.imshow("Egg Tracking",frame)

   
    key = cv2.waitKey(1) & 0xFF

    # Reset
    if key == ord("r") or key == ord("R"):
        count = 0
        counted_ids.clear()
        track_history.clear()
        print("Count Reset")

    # Quit
    if key == ord("q") or key == ord("Q"):
        break

# ==========================
# End
# ==========================
cap.release()
cv2.destroyAllWindows()