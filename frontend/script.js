const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");
const clearBtn = document.getElementById("clear-btn");
const predictBtn = document.getElementById("predict-btn");
const resultText = document.getElementById("result");

// Initialize canvas
ctx.fillStyle = "white";
ctx.fillRect(0, 0, canvas.width, canvas.height);
ctx.lineWidth = 10;
ctx.lineCap = "round";
ctx.strokeStyle = "black";

let drawing = false;

// Event Listeners for Drawing
canvas.addEventListener("mousedown", () => drawing = true);
canvas.addEventListener("mouseup", () => drawing = false);
canvas.addEventListener("mousemove", draw);

function draw(event) {
    if (!drawing) return;
    ctx.lineTo(event.offsetX, event.offsetY);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(event.offsetX, event.offsetY);
}

// Clear Canvas
clearBtn.addEventListener("click", () => {
    ctx.fillStyle = "white";
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    ctx.beginPath();
    resultText.textContent = "Prediction will appear here...";
});

// Convert canvas to Base64 & send to backend
predictBtn.addEventListener("click", async () => {
    const imageData = canvas.toDataURL("image/png").split(",")[1]; // Convert canvas to Base64
    const response = await fetch("https://your-api.render.com/predict", {  // Replace with your deployed API URL
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ image: imageData })
    });

    const data = await response.json();
    
    if (data.predictions) {
        resultText.innerHTML = data.predictions.map(p =>
            `Digit: ${p.digit}, Confi