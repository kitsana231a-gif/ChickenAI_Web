<script>

window.addEventListener("load", function () {

    function updateClock() {

        const t = document.getElementById("time");

        if (t) {
            t.textContent = new Date().toLocaleTimeString("th-TH");
        }

    }

    function updateDashboard() {

        fetch("/data")

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
            document.getElementById("device").textContent =
                data.device ?? "CPU";

            document.getElementById("model").textContent =
                data.model ?? "best1.pt";

            document.getElementById("tracker").textContent =
                data.tracker ?? "ByteTrack";

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

    fetch("/capture")

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

        fetch("/reset")

        .then(res => res.json())

        .then(data => {

            alert(data.message);

        });

    }

}

</script>
