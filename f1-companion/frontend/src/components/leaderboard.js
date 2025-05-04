// Extend base 

import React, { useEffect, useState } from 'react';

function LeaderboardComponent() {
    const [leaderboard, setLeaderboard] = useState(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const positionsRes = await fetch("http://127.0.0.1:5000/position-data");
                const leaderboardRes = await fetch("http://127.0.0.1:5000/leaderboard");

                if (!positionsRes.ok || !leaderboardRes.ok) {
                    throw new Error(`Leaderboard HTTP error: Position - ${positionsRes.status} | Leaderboard - ${leaderboardRes.status}`)
                }

                const positionsData = await positionsRes.json();
                const leaderboardData = await leaderboardRes.json();

                const sortedLeaderboard = leaderboardData.sort((a, b) => Number(a.position) - Number(b.position));

                setLeaderboard(sortedLeaderboard);
            } catch (error) {
                console.error(`Error fetching leaderboard data: ${error}`);
            }
        };

        fetchData();

        const intervalId = setInterval(fetchData, 3000);
        return () => clearInterval(intervalId);

    }, []);

    return (
        <div id="leaderboard">
            {leaderboard && leaderboard.length > 0 ? (
                <div>
                    <table border="1" cellpadding="5" cellspacing="0">
                        <thead>
                            <tr>
                                <td>Position</td>
                                <td>Number</td>
                                <td>Driver</td>
                                <td>Interval</td>
                                <td>Gap to Leader</td>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>1</td>
                                <td>{leaderboard[0].driver_number}</td>
                                <td>{leaderboard[0].name_acronym}</td>
                                <td>--</td>
                                <td>--</td>
                            </tr>
                            {leaderboard.slice(1).map((entry, index) => (
                                <tr key={index}>
                                    <td>{index + 2}</td>
                                    <td>{entry.driver_number}</td>
                                    <td>{entry.name_acronym}</td>
                                    <td>
                                        {entry.interval === "DNF" ? "DNF" : `+${entry.interval}`}
                                    </td>
                                    <td>
                                        {entry.gap_to_leader === "DNF" ? "DNF" : `+${entry.gap_to_leader}`}
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            ) : (
                <p>Loading leaderboard data...</p>
            )}
        </div>
    );
}

export default LeaderboardComponent;