import { Outlet } from "react-router-dom";
import Navigation from "./Navigation";
import useWebSocket from "../hooks/useWebSocket";
import Header from "./header"

export default function RaceDetail() {

    const {
        fastestLapUpdate,
        pitStopUpdate,
        raceControlUpdate,
        battleUpdate,
        leaderUpdate
    } = useWebSocket();
    
    return (
  <div className="min-h-screen bg-stone-600 font-mulish font-medium min-w-[410px] w-full ">

    <Header />

    <main className="absolute pt-6 pb-2 top-16 bottom-16 left-0 right-0 overflow-y-auto">
      <div className="max-w-4xl mx-auto p-4 text-white flex flex-col items-stretch">
        <Outlet />
      </div>
    </main>

    <div className="fixed bottom-0 left-0 right-0 h-16 z-50 bg-black">
      <Navigation />
    </div>
  </div>
);
}