

import React, { useEffect, useState } from 'react';

function RCHistoryComponent() {
    const [rcHistory, setRCHistory] = useState(null);

    useEffect(() => {
        const fetchRCHistory = async () => {
            try {
                const res = await fetch("http://127.0.0.1:5000/race-control")
                if (!res.ok) {
                    throw new Error(`Race Control HTTP error: ${res.status}`);
                }
                const data = await res.json();
                
                setRCHistory(data);
            } catch (error) {
                console.error(`Error fetching race control data: ${error}`);
            }
        };

        fetchRCHistory();

        const intervalId = setInterval(fetchRCHistory, 15000);
        return () => clearInterval(intervalId);

    }, []);

    return (
        <div id="rcHistory">
            {rcHistory && rcHistory.length > 0 ? (
                <div>
                    
                    <table border="1" cellpadding="5" cellspacing="0">
                        <thead>
                            <tr>
                                <td>Lap Number</td>
                                <td>Flag</td>
                                <td>Message</td>
                            </tr>
                        </thead>
                        <tbody>
                            {rcHistory.map((entry, index) => (
                                <tr key={index}>
                                    <td>{entry.lap_number}</td>
                                    <td>{entry.flag}</td>
                                    <td>{entry.message}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>

                </div>
            ) : (
                <p>Loading race control history...</p>
            )}
        </div>
    );
}

export default RCHistoryComponent;