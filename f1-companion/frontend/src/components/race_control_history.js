import React, { useEffect, useState } from 'react';
import useWebSocket from "../hooks/useWebSocket";

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

                const sortedData = data.reverse();
                
                setRCHistory(sortedData);
            } catch (error) {
                console.error(`Error fetching race control data: ${error}`);
            }
        };

        fetchRCHistory();

        const intervalId = setInterval(fetchRCHistory, 15000);
        return () => clearInterval(intervalId);

    }, []);

    const {
            raceControlUpdate
        } = useWebSocket();

    return (
        <section>
        <div id="rcHistory">
            <h1 className="font-bold text-xl text-center">
                RACE CONTROL MESSAGES
                <br></br>
                <br></br>
                </h1>
            {rcHistory && rcHistory.length > 0 ? (
                <div className="flex-1 grid gap-3 overflow-y-auto">
                    {rcHistory.map((msg, index) => (
                        <div
                            key={index}
                            className="flex items-center justify-center bg-stone-700 text-center text-white rounded-lg p-2 shadow-md border-red-600 border-2 h-32 sm:h-24">
                            <p className="break-words leading-snug">{msg.message}</p>
                        </div>
                    ))}
                    
                </div>
            ) : (
                <p className="text-center font-bold">Loading race control history...</p>
            )}
        </div>
        <div className="hidden">
            <strong>Race Control Alerts:</strong>
            <ul>
                {raceControlUpdate.map((u, i) => <li key={i}>{JSON.stringify(u)}</li>)}
            </ul>
        </div>
        </section>
    );
}

export default RCHistoryComponent;