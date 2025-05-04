// Extend base 

import React, { useEffect, useState } from 'react';

function CircuitComponent() {
    const [circuit, setCircuit] = useState(null);

    useEffect(() => {
        const fetchCircuit = () => {
            fetch("http://127.0.0.1:5000/circuits")
            .then(response => response.json())
            .then(data => {
                console.log("Fetched circuit data:", data);
                setCircuit(data);
            })
            .catch(err => console.error("Error fetching circuits:", err));
        };

        fetchCircuit();

        const intervalId = setInterval(fetchCircuit, 10000);
        return () => clearInterval(intervalId);
    }, []);

    console.log("Current circuit state: ", circuit);

    return (
        <div>
            {circuit && circuit.length > 0 ? (
                circuit.map((item, index) => (
                    <div key={index}>
                        <p>Country Name: {item.country_name ? item.country_name : "N/A"}</p>
                        <p>Location: {item.location ? item.location : "N/A"}</p>
                        <p>Session Type: {item.session_name ? item.session_name : "N/A"}</p>
                        <p>Local Time: {item.date_time_local ? item.date_time_local : "N/A"}</p>
                        <p>British Time: {item.date_time_gmt ? item.date_time_gmt : "N/A"}</p>
                        <p>Meeting Name: {item.meeting_official_name ? item.meeting_official_name : "N/A"}</p>
                        <p>Year: {item.year ? item.year : "N/A"}</p>
                        <hr />
                    </div>
                ))
            ) : (
                <p>Loading circuit data...</p>
            )}
        </div>
    );
}

export default CircuitComponent;