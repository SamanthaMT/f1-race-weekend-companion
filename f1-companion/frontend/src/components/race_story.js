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
        <section className="">
            <div id="race-story">
                <h1 className="font-bold text-xl text-center">
                    RACE STORY
                    <br></br>
                    <br></br>
                </h1>
                {raceStory && raceStory.length > 0 ? (
                    <div className="flex justify-center w-full overflow-x-auto">

                        <table className="w-full table-auto border-collapse" border="1" cellpadding="5" cellspacing="0">
                            <thead className="font-bold text-md bg-red-600 border-red-600">
                                <tr>
                                    <td className="p-3 rounded-tl-lg">CURRENT POSITION</td>
                                    <td className="p-3">NUMBER</td>
                                    <td className="p-3">DRIVER</td>
                                    <td className="p-3">STARTING POSITION</td>
                                    <td className="p-3 rounded-tr-lg">CHANGE</td>
                                </tr>
                            </thead>
                            <tbody>
                                {raceStory.map((entry, index) => (
                                    <tr key={index} className="border-b-2 border-red-600 odd:bg-stone-700/50">
                                        <td className="p-3">{entry.position}</td>
                                        <td className="p-3">{entry.driver_number}</td>
                                        <td className="p-3">{entry.name_acronym}</td>
                                        <td className="p-3">{entry.starting_position}</td>
                                        <td className={`p-3 font-bold ${
                                            `${entry.position_change}`.startsWith('+') ? 'text-lime-400' :
                                            `${entry.position_change}`.startsWith('-') ? 'text-red-300' :
                                            'text-white'
                                        }`}>{entry.position_change ?? "--"}</td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                ) : (
                    <p className="text-center font-bold">Loading race story data...</p>
                )}
            </div>
        </section>
    );
}

export default RaceStoryComponent;