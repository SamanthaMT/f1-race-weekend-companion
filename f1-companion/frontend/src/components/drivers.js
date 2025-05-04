// Extend base 

import React, { useEffect, useState } from 'react';

function DriverComponent() {
    const [driver, setDriver] = useState(null);

    useEffect(() => {
        const fetchDriver = () => {
            fetch("http://127.0.0.1:5000/drivers")
            .then(response => response.json())
            .then(data => {
                console.log("Fetched driver data:", data);
                setDriver(data);
            })
            .catch(err => console.error("Error fetching drivers:", err));
        };

        fetchDriver();

        const intervalId = setInterval(fetchDriver, 10000);
        return () => clearInterval(intervalId);
    }, []);

    console.log("Current driver state: ", driver);

    return (
        <div>
            {driver && driver.length > 0 ? (
                driver.map((item, index) => (
                    <div key={index}>
                        <p>Nationality: {item.country_code ? item.country_code : "N/A"}</p>
                        <p>Driver Number: {item.driver_number ? item.driver_number : "N/A"}</p>
                        <p>Driver Name: {item.full_name ? item.full_name : "N/A"}</p>
                        <p>Headshot URL: {item.headshot_url ? item.headshot_url : "N/A"}</p>
                        <p>Driver Last Name: {item.last_name ? item.last_name : "N/A"}</p>
                        <p>Name Acronym: {item.name_acronym ? item.name_acronym : "N/A"}</p>
                        <p>Team Colour: {item.team_colour ? item.team_colour : "N/A"}</p>
                        <p>Team Name: {item.team_name ? item.team_name : "N/A"}</p>
                        <hr />
                    </div>
                ))
            ) : (
                <p>Loading driver data...</p>
            )}
        </div>
    );
}

export default DriverComponent;