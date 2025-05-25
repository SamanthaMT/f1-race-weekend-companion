import React, { useEffect, useState } from 'react';
import useWebSocket from "../hooks/useWebSocket";

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

    const {
        fastestLapUpdate
    } = useWebSocket();

    return (
        <section className="flex flex-col">
        <div className="">
            <h1 className="font-bold text-xl text-center">
                FASTEST LAP
            </h1>

            {fastestLap ? (
                <div className="mt-20 sm:mt-10 flex flex-col items-center gap-8">
                    <div className="w-full max-w-xs sm:max-w-sm aspect-[18/11]">
                        <img src={fastestLap.headshot_url ?? "/images/tyres.jpg"}
                        alt={`Fastest lap by ${fastestLap.last_name ?? "Unknown Driver"}`}
                        title={fastestLap.headshot_url}
                        className="w-full h-full object-cover rounded-2xl shadow-md border-8"
                        style={{
                            borderColor: `#${fastestLap.team_colour ?? "dc2626"}`
                        }}
                        />
                    </div>
                    <div className="space-y-2 mt-2">
                        <p>
                            <strong className="font-bold">NUMBER :</strong> {fastestLap.driver_number ?? "N/A"}
                        </p>
                        <p>
                            <strong className="font-bold">DRIVER :</strong> {fastestLap.last_name?.toUpperCase() ?? "N/A"}
                        </p>
                        <p>
                            <strong className="font-bold">LAP NUMBER :</strong> {fastestLap.lap_number ?? "N/A"}
                        </p>
                        <p>
                            <strong className="font-bold">LAP DURATION :</strong> {fastestLap.lap_duration ?? "N/A"}
                        </p>
                        <p>
                            <strong className="font-bold">TOP SPEED :</strong>{" "}{fastestLap.top_speed != null ? `${fastestLap.top_speed}km/h` : "N/A"}
                        </p>
                    </div>
                </div>
            ) : (
                <p className="mt-7 text-center font-bold">Loading fastest lap data...</p>
            )}
        </div>
        <div className="hidden">
            <strong>Fastest-Lap Alerts:</strong>
            <ul>
                {fastestLapUpdate.map((u, i) => <li key={i}>{JSON.stringify(u)}</li>)}
            </ul>
        </div>
        </section>
    );
}

export default FastestLapComponent;
