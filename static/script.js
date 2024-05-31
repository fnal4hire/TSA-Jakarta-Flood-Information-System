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
            document.getElementById('max').innerText = `Max Temp: ${max}°C`;
            document.getElementById('min').innerText = `Min Temp: ${min}°C`;
        })
        .catch(error => {
            console.error('Error fetching weather data:', error);
            document.getElementById('weather').innerText = 'Failed to retrieve weather data';
        });
    //fetch weather forecast
    const forecastUrl = `https://api.openweathermap.org/data/2.5/forecast?lat=-6.200000&lon=106.816666&units=metric&appid=ea0b8aae6963a492e37462c3b9c835ce`;
    fetch(forecastUrl)
        .then(response=>response.json())
        .then(forecast=>{

            const forecastList = forecast.list;
            const forecastcontainer= document.getElementById('5-days');
            forecastcontainer.innerHTML = '';
            const addeddates = {};
            forecastList.forEach(daysdata=>{
                const datetime=daysdata.dt_txt;
                const date = datetime.split(' ')[0];
                if(!addeddates[date]){
                    const time=datetime.split(' ')[1];
                    if (time==='12:00:00'){
                        const days_desc=daysdata.weather[0].description;
                        const days_temp = daysdata.main.temp;
                        const days_humidity = daysdata.main.humidity;
                        const days_min=daysdata.main.temp_min;
                        const days_max=daysdata.main.temp_max;
                        const forecastItem = document.createElement('div');
                        forecastItem.className = 'forecast-item';

                        forecastItem.innerHTML = `
                        <h3>${date}</h3>
                        <p>Description: ${days_desc}</p>
                        <p>Temperature: ${days_temp}°C</p>
                        <p>Min Temp: ${days_min}°C, Max Temp: ${days_max}°C</p>
                        <p>Humidity: ${days_humidity}%</p>`;

                        forecastcontainer.appendChild(forecastItem);
                    }
                }
            });
        });
    // Function to update the clock
    function updateClock() {
        const clockElement = document.getElementById('clock');
        const now = new Date();
        const hours = now.getHours().toString().padStart(2, '0');
        const minutes = now.getMinutes().toString().padStart(2, '0');
        const seconds = now.getSeconds().toString().padStart(2, '0');
        const clockString = `${hours}:${minutes}:${seconds}`;
        clockElement.textContent = clockString;
    }

    // Update the clock initially
    updateClock();

    // Update the clock every second
    setInterval(updateClock, 1000);
});
