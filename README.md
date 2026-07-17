\# 🥚 Egg Counting AI Dashboard



ระบบตรวจนับไข่อัตโนมัติด้วย AI โดยใช้ YOLOv8 และ Flask สำหรับแสดงผลแบบ Real-time



\---



\## 📷 ตัวอย่างระบบ



> สามารถใส่รูปหน้าจอ Dashboard ได้ภายหลัง



\---



\## ✨ คุณสมบัติ



\- 🥚 ตรวจจับและนับจำนวนไข่ด้วย YOLOv8

\- 📹 แสดงภาพจากกล้องแบบ Real-time

\- 📈 แสดงจำนวนไข่ปัจจุบัน

\- 📊 แสดงจำนวนไข่สะสม

\- 🎯 แสดงค่า Confidence

\- ⚡ แสดงค่า FPS

\- 📋 บันทึกประวัติการตรวจจับ

\- 💾 ดาวน์โหลดผลลัพธ์เป็นไฟล์ CSV

\- 🌐 Dashboard ผ่าน Flask



\---



\## 🛠 เทคโนโลยีที่ใช้



\- Python

\- YOLOv8 (Ultralytics)

\- OpenCV

\- Flask

\- HTML

\- CSS

\- JavaScript



\---



\## 📂 โครงสร้างโปรเจกต์



```

ChickenAI\_Web/

│

├── app.py

├── detector\_web.py

├── detector.py

├── database.py

├── requirements.txt

├── best1.pt

│

├── templates/

│   └── index.html

│

├── static/

│   └── css/

│       └── style.css

│

└── Data/

```



\---



\## 🚀 วิธีติดตั้ง



ติดตั้งไลบรารี



```bash

pip install -r requirements.txt

```



\---



\## ▶ วิธีรัน



```bash

python app.py

```



จากนั้นเปิด



```

http://127.0.0.1:5000

```



\---



\## 📊 Dashboard



Dashboard แสดงข้อมูลแบบ Real-time



\- จำนวนไข่ปัจจุบัน

\- จำนวนไข่สะสม

\- Confidence

\- FPS

\- AI Status

\- เวลา

\- ประวัติการตรวจจับ

\- ดาวน์โหลด CSV



\---



\## 👨‍💻 ผู้พัฒนา



\*\*Kitsana\*\*
\*\*Nuttapoom\*\*



\---



\## 📄 License



ใช้เพื่อการศึกษาและพัฒนาระบบ AI

