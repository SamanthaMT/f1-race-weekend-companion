import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import Header from "./header";
import { toast } from "react-toastify";

export default function RaceList() {
    const navigate = useNavigate();
    const [races, setRaces] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        console.log("Attempting to fetch circuits...")
        fetch ("http://127.0.0.1:5000/circuits")
        .then((response) => response.json())
        .then((data) => {
            setRaces(data);
            setLoading(false);
        })
        .catch((err) => {
            console.error("Failed to fetch race list:", err);
            setLoading(false);
        });
    }, []);

    function handleClick(race) {
        if (race.status === "current") {
            navigate(`/race/${race.id}/leaderboard`);
        } else if (race.status === "past") {
            toast(`${race.location} ${race.session_name} winner was: ${race.full_name} (${race.driver_number})`)
        } else {
            toast.success(`"${race.meeting_official_name}" is coming soon!`);
        }
    }

    if (loading) return <p className="p-6 text-white font-bold text-center">Loading race list...</p>;

    return (
        <div className="min-h-screen text-center min-w-[410px] w-full">
            <Header />
            <main className="absolute font-mulish top-16 bottom-0 pt-4 left-0 right-0 overflow-y-auto items-stretch">
                <div className="py-4 flex flex-col gap-4 w-full items-stretch">
                    {races.map((race) => (
                        <div 
                        key={race.id}
                        onClick={() => handleClick(race)}
                        className={`
                            group border-t-8 border-b-8 grid grid-cols-3 p-2 shadow cursor-pointer h-48 sm:h-36
                            ${race.status === "current" ? "bg-stone-100 hover:bg-red-600" : "bg-stone-700 cursor-default"}
                            `}
                        style={{
                            borderColor: `#${race.team_colour ?? "dc2626"}`
                        }}
                        >

                            <div className={`col-span-2 text-center p-2 ${race.status === "current" ? "text-black" : "text-white"}`}>
                                <h2 className="text-lg font-bold">{race.country_name}</h2>
                                <h3 className="">{race.meeting_official_name}</h3>
                                <h4 className="text-sm">{race.session_name}</h4>
                            </div>

                            <div className="col-span-1 justify-center group">
                                {race.status === "past" && (
                                    <>
                                        <img className="mx-auto object-cover aspect-square w-36 sm:w-24 h-36 sm:h-24"
                                        src={race.headshot_url}
                                        alt={`Race winner: ${race.full_name}`}
                                        title={race.headshot_url}/>
                                    </>
                                )}
                                {race.status === "future" && (
                                    <>
                                        <h4 className="text-white text-sm text-right">Local: {race.date_time_local}</h4>
                                        <h4 className="text-white text-sm text-right">GMT: {race.date_time_gmt}</h4>
                                        <p className="text-sm text-right italic text-gray-400">Coming Soon</p>
                                    </>
                                )}
                                {race.status === "current" && (
                                    <p className="flex justify-center text-2xl font-bold text-lime-700 group-hover:text-lime-400">Live Now</p>
                                )}
                            </div>
                        
                        </div>
                    ))}
                </div>
            </main>
        </div>
    );
}