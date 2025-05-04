

import React, { useEffect, useState } from 'react';

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

                const sortedPitData = pitStopData.sort((a, b) => new Date(a.date) - new Date(b.date));
          
                setPitStops(sortedPitData);
                } catch (error) {
                    console.error(`Error fetching pit data: ${error}`);
                }
            };

            fetchData();

            const intervalId = setInterval(fetchData, 15000);
            return () => clearInterval(intervalId);

        }, []);

    return (
        <div id="pitStop">
            <h2>Pit Stop Record</h2>
            {pitStop && pitStop.length > 0 ? (
                <div>
                    <table border="1" cellpadding="5" cellspacing="0">
                        <thead>
                            <tr>
                                <td>Number</td>
                                <td>Driver</td>
                                <td>Pit Stops</td>
                                <td>Pit Duration</td>
                                <td>Last Pit</td>
                                <td>Compound</td>
                                <td>Tyre Age</td>
                            </tr>
                        </thead>
                        <tbody>
                            {pitStop.map((entry, index) => (
                                <tr key={index}>
                                    <td>{entry.driver_number}</td>
                                    <td>{entry.name_acronym}</td>
                                    <td>{entry.pit_stops}</td>
                                    <td>{entry.pit_duration}s</td>
                                    <td>Lap {entry.lap_number}</td>
                                    <td>{entry.compound}</td>
                                    <td>{entry.tyre_age} Laps</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>

                </div>
            ) : (
                <p>Loading pit stop record...</p>
            )}
        </div>
    );
}

export default PitStopComponent;