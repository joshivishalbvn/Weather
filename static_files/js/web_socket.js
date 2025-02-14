var ws = null;  

const closeWebSocket = () => {
    if (ws) {
        console.log("Closing WebSocket connection.");
        ws.close();
        ws = null;
    }
};

const connectWebSocket = (city) => {

    closeWebSocket();
    
    console.log("web socket city",city)
    
    ws = new WebSocket(`ws://${window.location.host}/ws/data/${city}/`);
    console.log("ws",ws);

    ws.onopen = () => {
        console.log("Connected to WebSocket");
    };

    ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        console.log("Received message:", data);
        const citySelect = document.getElementById('id_city');
        const selectedCity = citySelect.value; 
        console.log("selectedCity:", selectedCity);

        let maxTempEle = document.getElementById("0_max_temp_id");
        let windSpeed = document.getElementById("0_wind_speed");
        let windDir = document.getElementById("0_wind_direction");
        const windDirectionText = getWindDirection(data.wind_direction);

        maxTempEle.textContent = data.temperature;
        windSpeed.textContent = data.wind_speed;
        windDir.textContent = windDirectionText;
    };

    ws.onclose = () => {
        console.log("Disconnected from WebSocket");
    };

};