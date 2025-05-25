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
        <section>
        <div className="flex flex-col">
            <h1 className="font-bold text-xl text-center">
                WEATHER
            </h1>
            
            {weather ? (
                <div className="mt-20 sm:mt-10 flex flex-col items-center gap-8">
                    <div className="w-full max-w-xs sm:max-w-sm aspect-[18/11]">
                        <img src={weather.rainfall == 1 ? "/images/rain.jpg" : "/images/sun.jpg"}
                        alt="Current weather"
                        className="w-full h-full object-cover rounded-2xl shadow-md border-8 border-red-600 aspect-video "
                        />
                    </div>
                    <div className="space-y-2 mt-2">
                        <p>
                            <strong className="font-bold">AIR TEMPERATURE :</strong>{" "}{weather.air_temperature != null ? `${weather.air_temperature}°C` : "N/A"}
                        </p>
                        <p>
                            <strong className="font-bold">HUMIDITY :</strong>{" "}{weather.humidity != null ? `${weather.humidity}%` : "N/A"}
                        </p>
                        <p><strong className="font-bold">RAINFALL : </strong>{weather.rainfall ?? "N/A"}</p>
                        <p>
                            <strong className="font-bold">TRACK TEMPERATURE :</strong>{" "}{weather.track_temperature != null ? `${weather.track_temperature}°C` : "N/A"}
                        </p>
                        <p>
                            <strong className="font-bold">WIND SPEED :</strong>{" "}{weather.wind_speed != null ? `${weather.wind_speed}m/s` : "N/A"}
                        </p>
                    </div>
                </div>
            ) : (
                <p className="mt-7 text-center font-bold">Loading weather data...</p>
            )}
        </div>
        </section>
    );
}

export default WeatherComponent;
