function getWindDirection(degrees) {
    if (degrees >= 0 && degrees < 45) {
        return "North";
    } else if (degrees >= 45 && degrees < 135) {
        return "East";
    } else if (degrees >= 135 && degrees < 225) {
        return "South";
    } else if (degrees >= 225 && degrees < 315) {
        return "West";
    } else if (degrees >= 315 && degrees < 360) {
        return "North";
    }
    return "Invalid direction"; 
}

function setWeatherData(weather_data){
    const forecastData = weather_data;

    for (let i = 0; i < forecastData.length; i++) {
        const dayForecast = forecastData[i];
        const day = i; 
        try {
            const max_temp = dayForecast.max_temp;
            const min_temp = dayForecast.min_temp;
            const windspeed_max = dayForecast.windspeed_max;
            const windDirection = dayForecast.wind_direction;
            const dayName = dayForecast.day_name;
            const date = dayForecast.date;

            let maxTempEle = document.getElementById(`${day}_max_temp_id`);
            let minTempEle = document.getElementById(`${day}_min_temp`);
            let dayNameEle = document.getElementById(`${day}_day_name`);

            dayNameEle.parentNode.parentNode.setAttribute('data-date', date); 

            maxTempEle.textContent = max_temp;
            dayNameEle.innerHTML = dayName;
            if (minTempEle) {
                minTempEle.textContent = min_temp;
            } else {
                console.error(`Element for day ${day} not found.`);
            }

            if (windspeed_max) {
                const windSpeedEle = document.getElementById(`${day}_wind_speed`);
                if (windSpeedEle) {
                    windSpeedEle.textContent = `${windspeed_max} km/h`;
                }
            }

            if (windDirection) {
                const windDirectionEle = document.getElementById(`${day}_wind_direction`);
                if (windDirectionEle) {
                    const windDirectionText = getWindDirection(windDirection);
                    windDirectionEle.textContent = windDirectionText;
                }
            }
        } catch (error) {
            console.error(`Error updating weather data for day ${day}:`, error);
        }
    }
}


function getUserLocation() {
    let dotCount = 0;
    const cityElement = document.getElementById('city_id');
    const tempElement = document.getElementById('today_temp_id');
    const loadingText = "Finding Location";
    
    function animateDots() {
        dotCount++;
        if (dotCount > 3) dotCount = 1; 
        cityElement.textContent = loadingText + '.'.repeat(dotCount);
    }

    const animationInterval = setInterval(animateDots, 500); 

    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {
            var latitude = position.coords.latitude;
            var longitude = position.coords.longitude;
            console.log("latitude", latitude);
            console.log("longitude", longitude);

            fetch('/location/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCSRFToken() 
                },
                body: JSON.stringify({
                    latitude: latitude,
                    longitude: longitude
                })
            })
            .then(response => response.json())
            .then(data => {
                console.log('Location sent:', data);
                
                clearInterval(animationInterval);

                if (data.location_info) {
                    cityElement.textContent = data.location_info.city; 
                    connectWebSocket(data.location_info.city);
                } else {
                    console.error('City not found in the response.');
                    cityElement.textContent = "Location Not Found";
                }
                if (data.weather_data) {
                    setWeatherData(data.weather_data)
                } else {
                    console.error('Temperature data not found in the response.');
                }
            })
            .catch((error) => {
                console.error('Error:', error);
                clearInterval(animationInterval);
                cityElement.textContent = "Error Getting Location";
            });
        }, function(error) {
            console.error("Error getting geolocation:", error);
            clearInterval(animationInterval);
            cityElement.textContent = "Error Getting Location";
        });
    } else {
        clearInterval(animationInterval);
        cityElement.textContent = "Geolocation Not Supported";
    }
}

window.onload = getUserLocation;