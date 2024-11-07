// API Keys
const api_key = 'ffd15dc166a2a58dee0b73e39a730c65';  // OpenWeatherMap API key
const nrel_api_key = 'qlNlaFYiDTUXDc9N0QjDz9kxDLOzEdHRyVjQii9q';  // NREL API key for solar data
const places_api_key = 'a4e640e5aemsh32e9befa10340e0p183ebajsn3276fcfeecf1'; // Google Places API key

// Initialize the map, set to a default location
var map = L.map('map').setView([51.505, -0.09], 13); // Default to London

// Add OpenStreetMap tiles
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
}).addTo(map);

var userMarker; // To hold the user's marker

// Function to get the user's current location
function getLocation() {
    if (navigator.geolocation) {
        document.getElementById('status').textContent = "Getting location...";
        navigator.geolocation.getCurrentPosition(showPosition, showError);
    } else {
        document.getElementById('status').textContent = "Geolocation is not supported by this browser.";
    }
}

function showPosition(position) {
    var lat = position.coords.latitude;
    var lon = position.coords.longitude;

    document.getElementById('status').textContent = "Location found!";
    map.setView([lat, lon], 13);

    // Fetch both wind speed and solar data
    fetchWeatherAndSolarData(lat, lon);
    
    // Fetch nearby solar system providers
    fetchNearbySolarProviders(lat, lon);
}

function fetchWeatherAndSolarData(lat, lon) {
    // Fetch wind speed from OpenWeatherMap API
    fetch(`https://api.openweathermap.org/data/2.5/weather?lat=${lat}&lon=${lon}&appid=${api_key}&units=metric`)
        .then(response => response.json())
        .then(windData => {
            const windSpeedMps = windData.wind?.speed;

            if (windSpeedMps === undefined) {
                console.error('Wind speed data is not available for this location');
                return;
            }

            const windSpeedKmh = windSpeedMps * 3.6; // Convert to km/h

            // Fetch solar data from NREL API
            fetch(`https://developer.nrel.gov/api/solar/solar_resource/v1.json?api_key=${nrel_api_key}&lat=${lat}&lon=${lon}`)
                .then(response => response.json())
                .then(solarData => {
                    console.log('Solar Data Response:', solarData);

                    const avgDNI = solarData.outputs?.avg_dni;
                    
                    // Remove previous marker if it exists
                    if (userMarker) {
                        map.removeLayer(userMarker);
                    }

                    let popupContent = `
                        <b>Wind Speed:</b> ${windSpeedKmh.toFixed(2)} km/h<br>
                    `;

                    if (avgDNI && avgDNI.annual && avgDNI.annual !== "no data") {
                        popupContent += `<b>Annual Average DNI:</b> ${avgDNI.annual.toFixed(2)} kWh/m²/day`;
                    } else {
                        popupContent += `<b>Solar Data:</b> Not available for this location`;
                    }

                    userMarker = L.marker([lat, lon]).addTo(map)
                        .bindPopup(popupContent).openPopup();
                })
                .catch(error => {
                    console.error('Error fetching solar data:', error);

                    let popupContent = `
                        <b>Wind Speed:</b> ${windSpeedKmh.toFixed(2)} km/h<br>
                        <b>Solar Data:</b> Error fetching solar data
                    `;

                    if (userMarker) {
                        map.removeLayer(userMarker);
                    }

                    userMarker = L.marker([lat, lon]).addTo(map)
                        .bindPopup(popupContent).openPopup();
                });
        })
        .catch(error => {
            console.error('Error fetching wind speed data:', error);
        });
}

function fetchNearbySolarProviders(lat, lon) {
    const url = `https://google-map-places.p.rapidapi.com/maps/api/place/nearbysearch/json`;

    const querystring = {
        location: `${lat},${lon}`,
        radius: '5000',  // Adjust radius as needed
        language: 'en',
        opennow: 'true',
        rankby: 'prominence',
        keyword: 'solar'  // Keywords to narrow the search
    };

    const headers = {
        "x-rapidapi-key": places_api_key,
        "x-rapidapi-host": "google-map-places.p.rapidapi.com"
    };

    fetch(`${url}?${new URLSearchParams(querystring)}`, {
        method: 'GET',
        headers: headers
    })
    .then(response => response.json())
    .then(data => {
        console.log('Solar System Providers Data:', data); // For debugging

        // Clear previous markers except userMarker
        map.eachLayer(layer => {
            if (layer instanceof L.Marker && layer !== userMarker) {
                map.removeLayer(layer);
            }
        });

        // Extract and display provider details on the map
        data.results.forEach(provider => {
            const { geometry, name, vicinity, rating, place_id } = provider;

            // Filter out irrelevant results if needed
            if (name.toLowerCase().includes('solar') || vicinity.toLowerCase().includes('solar')) {
                L.marker([geometry.location.lat, geometry.location.lng])
                    .addTo(map)
                    .bindPopup(`
                        <b>${name}</b><br>
                        Address: ${vicinity}<br>
                        Rating: ${rating ? rating : 'N/A'}<br>
                        <a href="https://www.google.com/maps/place/?q=place_id:${place_id}" target="_blank">View on Google Maps</a>
                    `);
            }
        });
    })
    .catch(error => {
        console.error('Error fetching solar system providers:', error);
    });
}

function showError(error) {
    switch(error.code) {
        case error.PERMISSION_DENIED:
            document.getElementById('status').textContent = "User denied the request for Geolocation.";
            break;
        case error.POSITION_UNAVAILABLE:
            document.getElementById('status').textContent = "Location information is unavailable.";
            break;
        case error.TIMEOUT:
            document.getElementById('status').textContent = "The request to get user location timed out.";
            break;
        case error.UNKNOWN_ERROR:
            document.getElementById('status').textContent = "An unknown error occurred.";
            break;
    }
}

function geocodeAddress() {
    var address = document.getElementById('addressInput').value;
    if (!address) {
        document.getElementById('status').textContent = "Please enter an address.";
        return;
    }

    var url = `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(address)}`;

    fetch(url)
        .then(response => response.json())
        .then(data => {
            if (data.length > 0) {
                var lat = data[0].lat;
                var lon = data[0].lon;

                document.getElementById('status').textContent = "Address found!";
                map.setView([lat, lon], 13);

                // Fetch wind speed, solar data, and nearby solar providers for the given address
                fetchWeatherAndSolarData(lat, lon);
                fetchNearbySolarProviders(lat, lon);
            } else {
                document.getElementById('status').textContent = "Address not found.";
            }
        })
        .catch(() => {
            document.getElementById('status').textContent = "Error fetching address.";
        });
}
