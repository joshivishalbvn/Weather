// Utility function to convert time to 12-hour format
function convertTo12HourFormat(time) {
  const hour = parseInt(time.substring(0, 2));
  const minute = time.substring(3, 5);
  let hour12 = hour % 12 || 12; // Convert to 12-hour format
  const ampm = hour < 12 ? 'AM' : 'PM';
  return { time12: `${hour12}:${minute} ${ampm}`, hour, minute };
}

// Utility function to get time of day and image name
function getTimeOfDay(hour) {
  let timeOfDay, image_name;
  if (hour >= 6 && hour < 12) {
    timeOfDay = 'morning';
    image_name = "morning.png";
  } else if (hour >= 12 && hour < 18) {
    timeOfDay = 'afternoon';
    image_name = "afternoon.png";
  } else if (hour >= 18 && hour < 21) {
    timeOfDay = 'evening';
    image_name = "evening.png";
  } else {
    timeOfDay = 'night';
    image_name = "moon.png";
  }
  return { timeOfDay, image_name };
}

// Function to load hourly weather
function loadHourlyWeather() {
  console.log(cityName);
  const weatherListContainer = document.querySelector('.hourly-weather-list');
  weatherListContainer.innerHTML = '';

  hourlyWeatherData.time.forEach((time, index) => {
    const { time12, hour } = convertTo12HourFormat(time); // Convert time to 12-hour format
    const { timeOfDay, image_name } = getTimeOfDay(hour); // Get time of day and image name

    const condition = hourlyWeatherData.weather_description[index] || 'Unknown';
    const temperature = hourlyWeatherData.temperature_2m[index];

    const iconUrl = `/static/images/icons/${image_name}`;

    const weatherItem = document.createElement('div');
    weatherItem.classList.add('hourly-weather-item');
    weatherItem.setAttribute('data-hour', time);

    weatherItem.innerHTML = `
        <img src="${iconUrl}" alt="${condition} (${timeOfDay})">
        <div class="time">${time12}</div>
        <div class="temp">${temperature}°C</div>
      `;

    weatherItem.onclick = function () {
      openModal(index);
    };

    weatherListContainer.appendChild(weatherItem);
  });
}

// Function to open modal and display weather details
function openModal(index) {
  const modal = document.getElementById('weather-modal');
  const modalDetails = document.getElementById('modal-details');

  const time = hourlyWeatherData.time[index];
  const visibility = hourlyWeatherData.visibility[index];
  const wind_gusts = hourlyWeatherData.wind_gusts_10m[index];
  const temp = hourlyWeatherData.temperature_2m[index];
  const condition = hourlyWeatherData.weather_description[index];
  const cloud_cover = hourlyWeatherData.cloud_cover[index];
  const humidity = hourlyWeatherData.relative_humidity_2m[index];
  const dewPoint = hourlyWeatherData.dew_point_2m[index];

  const { time12, hour } = convertTo12HourFormat(time); // Convert time to 12-hour format
  const { timeOfDay, image_name } = getTimeOfDay(hour); // Get time of day and image name

  const iconUrl = `/static/images/icons/${image_name}`;

  modalDetails.innerHTML = `
      <div class="modal-header" style="display: flex; align-items: center; justify-content: center; margin-bottom: 20px; text-align: center;">
        <div class="info-item" style="margin-right: 10px;">
          <img src="${iconUrl}" alt="${timeOfDay}" class="weather-icon" style="width: 50px; height: 50px;"/>
        </div>
        <strong class="weather-title" style="font-size: 1.2em; font-weight: bold; display: inline-block;">
          ${cityName}'s Weather Details for ${time12}
        </strong>
      </div>
      <div class="modal-info">
        <div class="info-item">
          <span>Time:</span>
          <span class="value">${time12}</span>
        </div>
        <div class="info-item">
          <span>Temperature:</span>
          <span class="value">${temp}°C</span>
        </div>
        <div class="info-item">
          <span>Humidity:</span>
          <span class="value">${humidity}%</span>
        </div>
        <div class="info-item">
          <span>Dew Point:</span>
          <span class="value">${dewPoint}°C</span>
        </div>
        <div class="info-item">
          <span>Wind Gusts:</span>
          <span class="value">${wind_gusts} km/h</span>
        </div>
        <div class="info-item">
          <span>Cloud Cover:</span>
          <span class="value">${cloud_cover}%</span>
        </div>
        <div class="info-item">
          <span>Visibility:</span>
          <span class="value">${visibility} km</span>
        </div>
        <div class="info-item">
          <span>Condition:</span>
          <span class="value">${condition}</span>
        </div>
      </div>
    `;

  modal.style.display = "block";
}

// Function to close modal
function closeModal() {
  const modal = document.getElementById('weather-modal');
  modal.style.display = "none";
}

// Close modal if clicked outside
window.onclick = function (event) {
  const modal = document.getElementById('weather-modal');
  if (event.target === modal) {
    closeModal();
  }
}

window.onload = loadHourlyWeather;
