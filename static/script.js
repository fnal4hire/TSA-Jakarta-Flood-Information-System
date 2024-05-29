document.addEventListener("DOMContentLoaded", function() {
    // Function to update the graph image based on selected pintu_air
    window.updatePintuAir = function() {
        const pintuAir = document.getElementById("pintu-air").value;
        const baseUrl = document.querySelector('.dashboard').getAttribute('data-graph-url');
        const graphPath = `${baseUrl}/${pintuAir.replace(/ /g, '_')}.png`;

        // Update the graph image
        const floodgateGraph = document.getElementById('floodgate-graph');
        floodgateGraph.src = graphPath;
        floodgateGraph.alt = `Graph for ${pintuAir}`;
    };

    // Attach event listener to the select element
    document.getElementById("pintu-air").addEventListener("change", updatePintuAir);

    // Function to fetch and display weather data for Jakarta
    const apiUrl = `https://api.openweathermap.org/data/2.5/weather?lat=-6.200000&lon=106.816666&units=metric&appid=ea0b8aae6963a492e37462c3b9c835ce`;

    fetch(apiUrl)
        .then(response => response.json())
        .then(data => {
            const city= data.name
            const description = data.weather[0].description;
            const temperature = data.main.temp;
            const max = data.main.temp_max;
            const min = data.main.temp_min;
            const humidity = data.main.humidity;

            document.getElementById('city').innerText = `${city}`;
            document.getElementById('description').innerText = `${description}`;
            document.getElementById('temp').innerText = `${temperature}°C`;
            document.getElementById('humidity').innerText = `${humidity}%`;
            document.getElementById('max').innerText = `Max Temp: ${max}%`;
            document.getElementById('min').innerText = `Min Temp: ${min}%`;
        })
        .catch(error => {
            console.error('Error fetching weather data:', error);
            document.getElementById('weather').innerText = 'Failed to retrieve weather data';
        });
});
