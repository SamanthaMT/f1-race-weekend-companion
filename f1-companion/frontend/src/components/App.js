/*import React from "react";
import useWebSocket from "../hooks/useWebSocket";
import WeatherComponent from "./weather";
import LeaderboardComponent from "./leaderboard";
import PitStopComponent from "./pit_stops";
import BattlesComponent from "./battle_record";
import RaceStoryComponent from "./race_story";
import RCHistoryComponent from "./race_control_history";
import FastestLapComponent from "./fastest_lap";
import CircuitComponent from "./circuits";
import DriverComponent from "./drivers";
//new for frontend work
import RaceList from "./RaceList";
import RaceCard from "./RaceCard";
import RaceDetail from "./RaceDetail";
import Navigation from "./Navigation";


function App() {
  const { socket, messages, fastestLapUpdate, pitStopUpdate, raceControlUpdate, battleUpdate, leaderUpdate } = useWebSocket();

  return (
    <div>
      <h1>F1 Race Data</h1>
      <div> 
        <h2>Server Messages</h2>
        <ul>
          {messages.map((update, index) => (
            <li key={index}>{JSON.stringify(update)}</li>
          ))}
        </ul>

        <h2>New Leader Alert</h2>
        <ul>
          {leaderUpdate.map((update, index) => (
            <li key={index}>{JSON.stringify(update)}</li>
          ))}
        </ul>

        <h2>Leaderboard</h2>
        <LeaderboardComponent />

        <h2>Battle History</h2>
        <BattlesComponent />


        <h2>Fastest Lap Alerts</h2>
        <ul>
          {fastestLapUpdate.map((update, index) => (
            <li key={index}>{JSON.stringify(update)}</li>
          ))}
        </ul>
        <FastestLapComponent />

        <h2>New Pit Stop Alert</h2>
        <ul>
          {pitStopUpdate.map((update, index) => (
            <li key={index}>{JSON.stringify(update)}</li>
          ))}
        </ul>
        <PitStopComponent />
        <h2>Race Control Alerts</h2>
        <ul>
          {raceControlUpdate.map((update, index) => (
          <li key={index}>{JSON.stringify(update)}</li>
          ))}
        </ul>   
        <h2>Race Control Message History</h2>
        <RCHistoryComponent />

        <h2>Race Story</h2>
        <RaceStoryComponent />
        
        <WeatherComponent />
    
        <h2>Driver List - put components in after testing live functions</h2>
        <h2>Circuit List - put components in after testing live functions</h2>
      

      </div>
    </div>
  );
}

export default App;
*/

import { Routes, Route, Navigate } from "react-router-dom";
import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import RaceList from "./RaceList";
import RaceDetail from "./RaceDetail";
import WeatherComponent from "./weather";
import LeaderboardComponent from "./leaderboard";
import PitStopComponent from "./pit_stops";
import BattlesComponent from "./battle_record";
import RaceStoryComponent from "./race_story";
import RCHistoryComponent from "./race_control_history";
import FastestLapComponent from "./fastest_lap";
import CircuitComponent from "./circuits";
import DriverComponent from "./drivers";

function App() {
  return (
    <div className="min-h-screen bg-stone-600 min-w-[410px] ">
    <Routes>
      {/* Render RaceDetail at root */}
      <Route path="/" element={<RaceList />} />

      <Route path="/race/:raceId/*" element={<RaceDetail/>}>

        {/* default tab = redirect from "/" → "/leaderboard" */}
        <Route index element={<Navigate to="leaderboard" replace />} />
        <Route path="home"          element={<RaceList />} />
        <Route path="leaderboard"   element={<LeaderboardComponent />} />
        <Route path="fastest-lap"   element={<FastestLapComponent />} />
        <Route path="battle-record" element={<BattlesComponent />} />
        <Route path="pit-stops"     element={<PitStopComponent />} />
        <Route path="race-control"  element={<RCHistoryComponent />} />
        <Route path="race-story"    element={<RaceStoryComponent />} />
        <Route path="weather"       element={<WeatherComponent />} />

        {/* catch-all: send unknown to leaderboard */}
        <Route path="*" element={<Navigate to="leaderboard" replace />} />
      </Route>

      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>

    <ToastContainer
        position="bottom-center"
        autoClose={8000}
        hideProgressBar={false}
        closeOnClick
      />
    </div>
  );
}

export default App;