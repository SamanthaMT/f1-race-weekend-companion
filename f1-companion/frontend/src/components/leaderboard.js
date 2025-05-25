import React, { useEffect, useState } from 'react';
import useWebSocket from "../hooks/useWebSocket";

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

    const {
        leaderUpdate
    } = useWebSocket();

    return (
        <section className="">
            <div id="leaderboard">
                <h1 className="font-bold text-xl text-center">
                    LEADERBOARD
                    <br></br>
                    <br></br>
                </h1>
                {leaderboard && leaderboard.length > 0 ? (
                    <div className="flex justify-center w-full overflow-x-auto">
                        <table className="w-full table-auto border-collapse" border="1" cellpadding="5" cellspacing="0">
                            <thead className="font-bold text-md bg-red-600 border-red-600">
                                <tr>
                                    <td className="p-3 rounded-tl-lg">Position</td>
                                    <td className="p-3">Number</td>
                                    <td className="p-3">Driver</td>
                                    <td className="p-3">Interval</td>
                                    <td className="p-3 rounded-tr-lg">Gap to Leader</td>
                                </tr>
                            </thead>
                            <tbody>
                                <tr className="border-b-2 border-red-600">
                                    <td className="p-3">1</td>
                                    <td className="p-3">{leaderboard[0].driver_number}</td>
                                    <td className="p-3">{leaderboard[0].name_acronym}</td>
                                    <td className="p-3">--</td>
                                    <td className="p-3">--</td>
                                </tr>
                                {leaderboard.slice(1).map((entry, index) => (
                                    <tr key={index} className="border-b-2 border-red-600 even:bg-stone-700/50">
                                        <td className="p-3">{index + 2}</td>
                                        <td className="p-3">{entry.driver_number}</td>
                                        <td className="p-3">{entry.name_acronym}</td>
                                        <td className="p-3">
                                            {typeof entry.interval === "number" ? `+${entry.interval}` : entry.interval}
                                        </td>
                                        <td className="p-3">
                                        {typeof entry.gap_to_leader === "number" ? `+${entry.gap_to_leader}` : entry.gap_to_leader}
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                ) : (
                    <p className="text-center font-bold">Loading leaderboard data...</p>
                )}
            </div>
            <div className="hidden">
                <strong>New Leader Alerts:</strong>
                <ul>
                    {leaderUpdate.map((u, i) => <li key={i}>{JSON.stringify(u)}</li>)}
                </ul>
            </div>
        </section>
    );
}

export default LeaderboardComponent;