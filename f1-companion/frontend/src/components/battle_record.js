import React, { useEffect, useState } from 'react';
import useWebSocket from "../hooks/useWebSocket";

function BattlesComponent() {
    const [battles, setBattles] = useState(null)
    const [ongoingBattles, setOngoingBattles] = useState(null)

    useEffect(() => {
        const fetchData = async () => {
            try {
                const carDataRes = await fetch("http://127.0.0.1:5000/car-data");
                const battlesRes = await fetch("http://127.0.0.1:5000/battles");
                const ongoingBattlesRes = await fetch("http://127.0.0.1:5000/ongoing-battles");

                if (!battlesRes.ok || !carDataRes.ok || !ongoingBattlesRes.ok) {
                    throw new Error(`HTTP error: Battles - ${battlesRes.status} | Car Data - ${carDataRes.status} | Ongoing Battles - ${ongoingBattlesRes.status}`);
                }

                const carData = await carDataRes.json();
                const battlesData = await battlesRes.json();
                const ongoingBattlesData = await ongoingBattlesRes.json();

                const sortedBattlesData = battlesData.reverse();
                const sortedOngoingBattlesData = ongoingBattlesData.reverse();
            
                setBattles(sortedBattlesData);
                setOngoingBattles(sortedOngoingBattlesData);
            } catch (error) {
                console.error(`Error fetching battle data: ${error}`);
            }
        };
        
        fetchData();

        const intervalId = setInterval(fetchData, 5000);
        return () => clearInterval(intervalId);

    }, []);

    const {
        battleUpdate
    } = useWebSocket();

    return (
        <section>
        <div id="ongoingBattles">
            <h1 className="font-bold text-xl text-center mb-8">
                CURRENT BATTLES
            </h1>
            {ongoingBattles && ongoingBattles.length > 0 ? (
                <div>
                    {ongoingBattles.map((entry, index) => (
                        <div 
                            key={index}
                            className="grid grid-cols-8 items-center gap-2 p-4 mb-2 border-2 border-red-600 rounded-lg text-white bg-stone-700">

                            <div className="col-span-3 text-center">
                                {entry.name_acronym} - {entry.driver_number}
                            </div>

                            <div className="col-span-2 text-center border-l-2 border-r-2 border-red-600">
                                LAP {entry.lap_number}
                            </div>

                            <div className="col-span-3 text-center">
                                {entry.ahead_name_acronym} - {entry.driver_ahead_number}
                            </div>
                        </div>
                    ))}
                    

                </div>
            ) : (
                <p className="text-center font-bold">No current battles</p>
            )}
        </div>
        <div id="battleRecord">
            <h1 className="font-bold text-xl text-center my-8">
                BATTLE HISTORY
            </h1>
            {battles && battles.length > 0 ? (
                <div>
                    {battles.map((entry, index) => (
                        <div 
                            key={index}
                            className="grid grid-cols-4 items-center gap-2 p-4 m-2 border-2 border-red-600 rounded-lg text-white bg-stone-700">

                            <div className="col-span-1 text-center border-r-2 border-red-600 ">
                                LAP {entry.lap_number}
                            </div>

                            <div className="col-span-3 text-center">
                                {entry.name_acronym} ({entry.driver_number}) - {entry.ahead_name_acronym} ({entry.driver_ahead_number})
                            </div>
                        </div>
                    ))}

                </div>
            ) : (
                <p className="text-center font-bold">Loading battle history...</p>
            )}
        </div>
        <div className="hidden">
        <strong>Battle Alerts:</strong>
        <ul>
            {battleUpdate.map((u, i) => <li key={i}>{JSON.stringify(u)}</li>)}
        </ul>
        </div>
        </section>
    );
}

export default BattlesComponent;