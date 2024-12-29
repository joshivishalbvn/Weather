function openModal(day) {
    const modal = document.getElementById("forecastModal");

    document.getElementById("modalDayName").innerText = day.querySelector('.day').innerText;
    document.getElementById("modalDate").innerText = day.querySelector('.date') ? day.querySelector('.date').innerText : 'N/A';
    document.getElementById("modalLocation").innerText = document.getElementById('city_id').innerText || 'Unknown';
    document.getElementById("modalHumidity").innerText = document.getElementById('0_humidity').innerText || 'N/A';
    document.getElementById("modalWindSpeed").innerText = document.getElementById('0_wind_speed').innerText || 'N/A';
    document.getElementById("modalWindDirection").innerText = document.getElementById('0_wind_direction').innerText || 'N/A';

    modal.style.display = "block";
}

function closeModal() {
    const modal = document.getElementById("forecastModal");
    modal.style.display = "none";
}

document.querySelector(".close-btn").addEventListener("click", closeModal);

window.addEventListener("click", function(event) {
    const modal = document.getElementById("forecastModal");
    if (event.target === modal) {
    closeModal();
    }
});

document.querySelectorAll('.forecast').forEach((forecastDay) => {
    forecastDay.addEventListener('click', () => openModal(forecastDay));
});