

import React, { useEffect, useState } from 'react';

function BattlesComponent() {
    const [battles, setBattles] = useState(null)

    useEffect(() => {
        const fetchData = async () => {
            try {
                const carDataRes = await fetch("http://127.0.0.1:5000/car-data");
                const battlesRes = await fetch("http://127.0.0.1:5000/battles");

                if (!battlesRes.ok || !carDataRes.ok) {
                    throw new Error(`HTTP error: Battles - ${battlesRes.status} | Car Data - ${carDataRes.status}`);
                }

                const carData = await carDataRes.json();
                const battlesData = await battlesRes.json();
            
                setBattles(battlesData);
            } catch (error) {
                console.error(`Error fetching battle data: ${error}`);
            }
        };
        
        fetchData();

        const intervalId = setInterval(fetchData, 5000);
        return () => clearInterval(intervalId);

    }, []);

    return (
        <div id="battle">
            {battles && battles.length > 0 ? (
                <div>
                    
                    <table border="1" cellpadding="5" cellspacing="0">
                        <thead>
                            <tr>
                                <td>Lap Number</td>
                                <td>Attacking Driver</td>
                                <td>Driver Ahead</td>
                            </tr>
                        </thead>
                        <tbody>
                            {battles.map((entry, index) => (
                                <tr key={index}>
                                    <td>{entry.lap_number}</td>
                                    <td>{entry.driver_number}</td>
                                    <td>{entry.driver_ahead_number}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>

                </div>
            ) : (
                <p>Loading battle history...</p>
            )}
        </div>
    );
}

export default BattlesComponent;