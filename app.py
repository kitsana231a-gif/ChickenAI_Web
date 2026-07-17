from flask import Flask, render_template, Response, jsonify, send_file
from flask_cors import CORS
import detector_web
from detector_web import generate_frames, get_status

import os

app = Flask(__name__)
CORS(app)

# ==========================
# หน้าเว็บ
# ==========================
@app.route("/")
def home():
    return render_template("index.html")


# ==========================
# วิดีโอ
# ==========================
@app.route("/video")
def video():
    return Response(
        generate_frames(),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )


# ==========================
# Dashboard Data
# ==========================
@app.route("/data")
def data():
    return jsonify(get_status())


# ==========================
# Capture Image
# ==========================
@app.route("/capture")
def capture():

    detector_web.capture_image()

    return jsonify({
        "success": True,
        "message": "Image Saved Successfully"
    })


# ==========================
# Reset Counter
# ==========================
@app.route("/reset")
def reset():

    detector_web.count = 0
    detector_web.counted_ids.clear()

    return jsonify({
        "success": True,
        "message": "Counter Reset Complete"
    })


# ==========================
# Download CSV
# ==========================
@app.route("/download_csv")
def download_csv():

    filepath = os.path.abspath(detector_web.csv_file)

    print("=" * 50)
    print("CSV PATH :", filepath)
    print("FILE EXISTS :", os.path.exists(filepath))
    print("=" * 50)

    if not os.path.exists(filepath):
        return "CSV File Not Found", 404

    return send_file(
        filepath,
        as_attachment=True,
        download_name=os.path.basename(filepath),
        mimetype="text/csv"
    )


# ==========================
# Run
# ==========================
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )