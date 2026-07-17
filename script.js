// =====================================
// URL ของ Backend
// =====================================
const API = "http://127.0.0.1:5000";
// ตัวอย่างตอนใช้ Cloudflare
// const API = "https://YOUR_CLOUDFLARE_URL.trycloudflare.com";

window.addEventListener("load", function () {

    // แสดงภาพกล้อง
    const camera = document.getElementById("camera-feed");
    if (camera) {
        camera.src = API + "/video";
    }

    // ลิงก์ดาวน์โหลด CSV
    const csv = document.getElementById("downloadCSV");
    if (csv) {
        csv.href = API + "/download_csv";
    }

    function updateClock() {

        const t = document.getElementById("time");

        if (t) {
            t.textContent = new Date().toLocaleTimeString("th-TH");
        }

    }

    function updateDashboard() {

        fetch(API + "/data")

        .then(res => res.json())

        .then(data => {

            document.getElementById("count").textContent =
                data.count ?? 0;

            document.getElementById("total").textContent =
                data.total ?? 0;

            document.getElementById("conf").textContent =
                Number(data.confidence ?? 0).toFixed(1);

            document.getElementById("fps").textContent =
                Number(data.fps ?? 0).toFixed(1);

            document.getElementById("status").textContent =
                data.status ?? "ONLINE";

            // AI Information
            const device = document.getElementById("device");
            if (device) {
                device.textContent = data.device ?? "CPU";
            }

            const model = document.getElementById("model");
            if (model) {
                model.textContent = data.model ?? "best1.pt";
            }

            const tracker = document.getElementById("tracker");
            if (tracker) {
                tracker.textContent = data.tracker ?? "ByteTrack";
            }

            let html = "";

            if (Array.isArray(data.history)) {

                data.history.forEach(item => {

                    html += `
                    <tr>
                        <td>${item.time}</td>
                        <td>${item.count}</td>
                    </tr>
                    `;

                });

            }

            document.getElementById("history").innerHTML = html;

        })

        .catch(function(err){

            console.log(err);

            document.getElementById("status").textContent = "OFFLINE";

        });

    }

    updateClock();
    updateDashboard();

    setInterval(updateClock,1000);
    setInterval(updateDashboard,500);

});

// ==========================
// Capture Image
// ==========================

function captureImage(){

    fetch(API + "/capture")

    .then(res => res.json())

    .then(data => {

        alert(data.message);

    });

}

// ==========================
// Reset Counter
// ==========================

function resetCounter(){

    if(confirm("ต้องการรีเซ็ตตัวนับหรือไม่ ?")){

        fetch(API + "/reset")

        .then(res => res.json())

        .then(data => {

            alert(data.message);

            location.reload();

        });

    }

}