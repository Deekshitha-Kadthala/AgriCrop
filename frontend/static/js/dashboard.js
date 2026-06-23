document.addEventListener("DOMContentLoaded", function () {

    const chartData = document.getElementById("chart-data");

    if (!chartData) {
        console.log("Chart data not found.");
        return;
    }

    const labels = JSON.parse(chartData.dataset.labels);
    const values = JSON.parse(chartData.dataset.values);

    console.log("Labels:", labels);
    console.log("Values:", values);

    if (labels.length === 0) {
        document.querySelector(".chart-container").innerHTML +=
            "<h3 style='text-align:center;color:gray;'>No prediction data available.</h3>";
        return;
    }

    const ctx = document.getElementById("diseaseChart").getContext("2d");

    new Chart(ctx, {
        type: "pie",

        data: {
            labels: labels,

            datasets: [{
                label: "Disease Statistics",
                data: values,

                backgroundColor: [
                    "#4CAF50",
                    "#2196F3",
                    "#FFC107",
                    "#FF5722",
                    "#9C27B0",
                    "#009688",
                    "#795548",
                    "#3F51B5",
                    "#8BC34A",
                    "#F44336"
                ],

                borderColor: "#ffffff",
                borderWidth: 2
            }]
        },

        options: {

            responsive: true,

            maintainAspectRatio: false,

            plugins: {

                legend: {
                    position: "bottom"
                }

            }

        }

    });

});