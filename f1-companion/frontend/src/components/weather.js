import React, { useEffect, useState } from 'react';

function WeatherComponent() {
    const [weather, setWeather] = useState(null); // State is null by default

    useEffect(() => {
        const fetchWeather = async () => {
            try {
                const res = await fetch("http://127.0.0.1:5000/weather")
                if (!res.ok) {
                    throw new Error(`Weather HTTP error: ${res.status}`);
                }
                const data = await res.json();
            
                if (data && typeof data === 'object' && !Array.isArray(data)) {
                    setWeather(data);
                } else {
                    setWeather(null);
                }
            } catch (error) {
                console.error("Error fetching weather data:", error);
            }
        };

        fetchWeather();
        const intervalId = setInterval(fetchWeather, 60000);
        return () => clearInterval(intervalId);
    }, []);

    return (
        <div>
            <h2>Weather Data</h2>
            {weather ? (
                <div>
                    <p>
                        Air Temperature:{" "}{weather.air_temperature != null ? `${weather.air_temperature}°C` : "N/A"}
                    </p>
                    <p>
                        Humidity:{" "}{weather.humidity != null ? `${weather.humidity}%` : "N/A"}
                    </p>
                    <p>Rainfall: {weather.rainfall ?? "N/A"}</p>
                    <p>
                        Track Temperature:{" "}{weather.track_temperature != null ? `${weather.track_temperature}°C` : "N/A"}
                    </p>
                    <p>
                        Wind Speed:{" "}{weather.wind_speed != null ? `${weather.wind_speed}m/s` : "N/A"}
                    </p>
                </div>
            ) : (
                <p>Loading weather data...</p>
            )}
        </div>
    );
}

export default WeatherComponent;
