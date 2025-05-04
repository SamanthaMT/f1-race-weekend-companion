import React, { useEffect, useState } from 'react';

function FastestLapComponent() {
    const [fastestLap, setFastestLap] = useState(null); // State is null by default

    useEffect(() => {
        const fetchFastestLap = async () => {
            try {
                const res = await fetch("http://127.0.0.1:5000/laps")
                if (!res.ok) {
                    throw new Error(`Lap HTTP error: ${res.status}`);
                }
                const data = await res.json()

                if (data && typeof data === 'object' && !Array.isArray(data)) {
                    setFastestLap(data);
                } else {
                    setFastestLap(null);
                }
            } catch (error) {
                console.error("Error fetching fastest lap data:", error);
            }
        };

        fetchFastestLap();
        const intervalId = setInterval(fetchFastestLap, 15000);
        return () => clearInterval(intervalId);
    }, []);

    return (
        <div>
            <h2>Fastest Lap Data</h2>
            {fastestLap ? (
                <div>
                    <p>Number: {fastestLap.driver_number ?? "N/A"}</p>
                    <p>Driver: {fastestLap.last_name?.toUpperCase() ?? "N/A"}</p>
                    <p>Lap Number: {fastestLap.lap_number ?? "N/A"}</p>
                    <p>Lap Duration: {fastestLap.lap_duration ?? "N/A"}</p>
                    <p>
                        Top Speed:{" "}{fastestLap.top_speed != null ? `${fastestLap.top_speed}km/h` : "N/A"}
                    </p>
                </div>
            ) : (
                <p>Loading fastest lap data...</p>
            )}
        </div>
    );
}

export default FastestLapComponent;
