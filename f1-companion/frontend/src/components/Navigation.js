
import { NavLink, useParams } from "react-router-dom"

const tabs = [
    { to: "/", label: <div className="flex items-center justify-center w-7 h-7 sm:w-6 sm:h-6 flex-shrink-0">
      <img src="/images/house.jpg" className="w-full h-full object-contain"/>
      </div> },
    { to: "leaderboard", label: "Leaderboard" },
    { to: "battle-record", label: "Battles" },
    { to: "pit-stops", label: "Pit Stops" },
    { to: "race-control", label: "Race Control" },
    { to: "fastest-lap", label: "Fastest Lap" },
    { to: "race-story", label: "Story" },
    { to: "weather", label: "Weather" }  
];

export default function Navigation() {
  const { raceId } = useParams();

  return (
    <nav className="w-full whitespace-nowrap overflow-x-auto space-x-4 px-2 py-4 sm:py-4 flex justify-around text-md bg-black ">
      {tabs.map((tab) => {
        const path = tab.to.startsWith("/")
        ? tab.to
        : `/race/${raceId}/${tab.to}`;
          
      return (
        <NavLink
          key={tab.to}
          to={path}
          className={({ isActive }) =>
            isActive ? " text-red-600 font-bold" : "text-white"
          }
        >
          {tab.label}
        </NavLink>
      );
      })}
    </nav>
  );
}