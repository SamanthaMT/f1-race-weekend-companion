// Extend base 

import React, { useEffect, useState } from 'react';

function RaceStoryComponent() {
    const [raceStory, setRaceStory] = useState(null);

    useEffect(() => {
        const fetchRaceStory = async () => {
            try {
                const res = await fetch("http://127.0.0.1:5000/race-story")

                if (!res.ok) {
                    throw new Error(`Race story HTTP error: ${res.status}`);
                }
                const data = await res.json();
                
                const sortedData = data.sort((a, b) => Number(a.position) - Number(b.position));

                setRaceStory(sortedData);
            } catch (error) {
                console.error(`Error fetching race story data: ${error}`);
            }
        };
            
        fetchRaceStory();

        const intervalId = setInterval(fetchRaceStory, 3000);
        return () => clearInterval(intervalId);
    }, []);



    return (
        <div id="race-story">
            {raceStory && raceStory.length > 0 ? (
                <div>
                    <table border="1" cellpadding="5" cellspacing="0">
                        <thead>
                            <tr>
                                <td>Current Position</td>
                                <td>Number</td>
                                <td>Driver</td>
                                <td>Starting Position</td>
                                <td>Change</td>
                            </tr>
                        </thead>
                        <tbody>
                            {raceStory.map((entry, index) => (
                                <tr key={index}>
                                    <td>{entry.position}</td>
                                    <td>{entry.driver_number}</td>
                                    <td>{entry.name_acronym}</td>
                                    <td>{entry.starting_position}</td>
                                    <td>{entry.position_change}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            ) : (
                <p>Loading race story data...</p>
            )}
        </div>
    );
}

export default RaceStoryComponent;