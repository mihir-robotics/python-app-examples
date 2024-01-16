document.addEventListener("DOMContentLoaded", function () {
    // Function to update sensor data
    function updateSensorData() {
        fetch('/get-data')  // Assuming this is the endpoint to get the latest sensor data
            .then(response => response.json())
            .then(data => {
                // Update the content of the sensorData div
                document.getElementById('sensorData').innerText = `Temperature: ${data.temperature}°C  |  Humidity: ${data.humidity}%`;
            })
            .catch(error => {
                console.error('Error fetching sensor data:', error);
            });
    }
    // Call updateSensorData initially
    updateSensorData();

    // Update sensor data every 5 seconds (adjust the interval as needed)
    setInterval(updateSensorData, 1000);
});
