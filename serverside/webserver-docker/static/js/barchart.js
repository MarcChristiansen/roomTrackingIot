const chartElement = document.querySelector("#barChart");

const labels = [01, 02, 03, 04, 05, 06, 07, 08, 09, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]

const data = {
    labels: labels,
    datasets: [{
        label: "Trend",
        data: [80, 80, 80, 70, 70, 20, 10, 5, 100, 100, 60],
        backgroundColor: "rgba(54, 162, 235, 0.2)",
        borderColor: "rgb(54, 162, 235)",
        borderWidth: 1
    }]
}

const config = {
    type: "bar",
    data: data,
    options: {
        responsive: true,
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
}

const chart = new Chart(chartElement, config);