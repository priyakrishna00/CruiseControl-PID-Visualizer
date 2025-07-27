document.getElementById("toggle-mode").addEventListener("click", () => {
  document.body.classList.toggle("light");
});

function resetSimulation() {
  document.getElementById("current-speed").innerText = "0";
  if (window.myChart) window.myChart.destroy();
}

async function runSimulation() {
  const kp = parseFloat(document.getElementById("kp").value);
  const ki = parseFloat(document.getElementById("ki").value);
  const kd = parseFloat(document.getElementById("kd").value);

  const response = await fetch("/simulate", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ kp, ki, kd })
  });

  const data = await response.json();
  const ctx = document.getElementById("chart").getContext("2d");

  document.getElementById("current-speed").innerText = data.speed[data.speed.length - 1].toFixed(1);

  if (window.myChart) window.myChart.destroy();
  window.myChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: data.time,
      datasets: [{
        label: "Speed (mph)",
        data: data.speed,
        borderColor: "rgb(0, 240, 255)",
        fill: false,
        tension: 0.3
      }]
    },
    options: {
      scales: {
        x: { title: { display: true, text: 'Time (s)' } },
        y: { title: { display: true, text: 'Speed (mph)' } }
      }
    }
  });
}
