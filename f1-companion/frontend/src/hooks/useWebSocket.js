import { useEffect, useState } from "react";
import { io } from "socket.io-client";
import { toast } from "react-toastify";


const useWebSocket = () => {
    const [socket, setSocket] = useState([]);
    const [messages, serverMessage] = useState([]);
    const [fastestLapUpdate, setFastestLapUpdate] = useState([]);
    const [pitStopUpdate, setPitStopUpdate] = useState([]);
    const [raceControlUpdate, setRaceControlUpdate] = useState([]);
    const [battleUpdate, setBattleUpdate] = useState([]);
    const [leaderUpdate, setLeaderUpdate] = useState([]);


    useEffect(() => {
        const threshold = new Date(Date.now() - 2 * 60 * 1000);
        //For testing - using exact datetime
        //const threshold = new Date("2025-05-24T14:30:00Z")

        const socketInstance = io("http://127.0.0.1:5000", {
            transports: ["websocket", "polling"]
        });
        setSocket(socketInstance);

        socketInstance.on("connect", () => {
            console.log("Connected to WebSocket server, sid=", socketInstance.id);
        });

        socketInstance.on("server_message", (data) => {
            console.log("Message from server:", data);
            serverMessage((prev) => [...prev, data]);
        });

        socketInstance.on("fastest_lap_update", (data) => {
            console.log("Fastest Lap Update:", data);
            setFastestLapUpdate(prev => {
                const updated = [...prev, data];
                return updated.length > 3 ? updated.slice(-3) : updated;
            });

            data.filter(lap => {
                const time = new Date(lap.date);
                return time > threshold;
            }).forEach(lap => {
                toast(`New Fastest Lap: ${lap.driver_number} - ${lap.name_acronym}`);
            });
        });

        socketInstance.on("pit_stop_update", (data) => {
            console.log("New Pit Stop:", data);
            setPitStopUpdate(prev => {
                const updated = [...prev, ...data];
                return updated.length > 3 ? updated.slice(-3) : updated;
            });
            
            data.filter(pit => {
                const time = new Date(pit.date);
                console.log(`threshold: ${threshold}`)
                console.log(`time: ${time}`)
                return time > threshold;
            }).forEach(pit => {
                toast(`Pit Stop: Driver ${pit.driver_number} - ${pit.name_acronym} (lap ${pit.lap_number})`);
            });
        });

        socketInstance.on("race_control_update", (data) => {
            console.log("Race Control Update:", data);
            setRaceControlUpdate(prev => {
                const updated = [...prev, ...data];
                return updated.length > 3 ? updated.slice(-3) : updated;
            });
            
            data.filter(msg => {
                const time = new Date(msg.date);
                return time > threshold;
            }).forEach(msg => {
                toast(`Race Control: ${msg.message} (lap ${msg.lap_number})`);
            });
        });

        socketInstance.on("battle_update", (data) => {
            console.log("New Battle Update:", data);
            setBattleUpdate(prev => {
                const updated = [...prev, ...data];
                return updated.length > 3 ? updated.slice(-3) : updated;
            });

            data.forEach(battle => {
                toast(`New battle between drivers ${battle.driver_number} and ${battle.driver_ahead_number}`);
            });
        });

        socketInstance.on("leader_update", (data) => {
            console.log("New Leader Update:", data);
            setLeaderUpdate(prev => {
                const updated = [...prev, ...data];
                return updated.length > 3 ? updated.slice(-3) : updated;
            });

            data.filter(leader => {
                const time = new Date(leader.date);
                return time > threshold;
            }).forEach(leader => {
                toast(`New Leader Alert: ${leader.driver_number} - ${leader.name_acronym}`);
            });
        });

        return () => {
            socketInstance.off("connect");
            socketInstance.off("fastest_lap_update");
            socketInstance.off("pit_stop_update");
            socketInstance.off("race_control_update");
            socketInstance.off("battle_update");
            socketInstance.off("leader_update")
            socketInstance.off("heartbeat")
            socketInstance.disconnect();
        };
    }, []);

    return { 
        socket, 
        messages, 
        fastestLapUpdate,
        pitStopUpdate,
        raceControlUpdate, 
        battleUpdate,
        leaderUpdate
    };
};

export default useWebSocket;
