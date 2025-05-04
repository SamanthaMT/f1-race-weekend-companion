import React from "react";
import useWebSocket from "./hooks/useWebSocket";
import WeatherComponent from "./components/weather";
import LeaderboardComponent from "./components/leaderboard";
import PitStopComponent from "./components/pit_stops";
import BattlesComponent from "./components/battle_record";
import RaceStoryComponent from "./components/race_story";
import RCHistoryComponent from "./components/race_control_history";
import FastestLapComponent from "./components/fastest_lap";
import CircuitComponent from "./components/circuits";
import DriverComponent from "./components/drivers";


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
