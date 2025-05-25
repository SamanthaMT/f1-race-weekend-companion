import React, { useEffect, useState } from 'react';
import useWebSocket from "../hooks/useWebSocket";

function PitStopComponent() {
    const [pitStop, setPitStops] = useState(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const stintsRes = await fetch("http://127.0.0.1:5000/stints");
                const pitStopRes = await fetch("http://127.0.0.1:5000/pits");

                if (!stintsRes.ok || !pitStopRes.ok) {
                    throw new Error(`HTTP error: Stints - ${stintsRes.status} | Pit Stops - ${pitStopRes.status}`)
                }

                const stintsData = await stintsRes.json();
                const pitStopData = await pitStopRes.json();

                const sortedPitData = pitStopData.sort((a, b) => new Date(b.date) - new Date(a.date));
          
                setPitStops(sortedPitData);
                } catch (error) {
                    console.error(`Error fetching pit data: ${error}`);
                }
            };

            fetchData();

            const intervalId = setInterval(fetchData, 15000);
            return () => clearInterval(intervalId);

        }, []);

        const {
            pitStopUpdate
        } = useWebSocket();

    return (
        <section className="">
            <div id="pitStop">
                <h1 className="font-bold text-xl text-center">
                    PIT STOP RECORD
                    <br></br>
                    <br></br>
                </h1>
                {pitStop && pitStop.length > 0 ? (
                    <div className="flex justify-start sm:justify-center w-full overflow-x-auto">
                        <table className="min-w-full table-auto border-collapse" border="1" cellpadding="5" cellspacing="0">
                            <thead className="font-bold text-md bg-red-600 border-red-600">
                                <tr>
                                    <td className="p-3 rounded-tl-lg">NUMBER</td>
                                    <td className="p-3">DRIVER</td>
                                    <td className="p-3">PIT STOPS</td>
                                    <td className="p-3">DURATION</td>
                                    <td className="p-3">LAST PIT</td>
                                    <td className="p-3">COMPOUND</td>
                                    <td className="p-3 rounded-tr-lg">AGE</td>
                                </tr>
                            </thead>
                            <tbody>
                                {pitStop.map((entry, index) => (
                                    <tr key={index} className="border-b-2 border-red-600 odd:bg-stone-700/50">
                                        <td className="p-3">{entry.driver_number}</td>
                                        <td className="p-3">{entry.name_acronym}</td>
                                        <td className="p-3">{entry.pit_stops}</td>
                                        <td className="p-3">{entry.pit_duration != null ? `${entry.pit_duration}s` : ""}</td>
                                        <td className="p-3">{entry.lap_number != null ? `Lap ${entry.lap_number}` : ""}</td>
                                        <td className="p-3">{entry.compound}</td>
                                        <td className="p-3">{entry.tyre_age != null ? `${entry.tyre_age} Laps` : ""}</td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                ) : (
                    <p className="text-center font-bold">Loading pit stop record...</p>
                )}
            </div>
            <div className="hidden">
                <strong>Pit-Stop Alerts:</strong>
                <ul>
                    {pitStopUpdate.map((u, i) => <li key={i}>{JSON.stringify(u)}</li>)}
                </ul>
            </div>
        </section>
    );
}

export default PitStopComponent;