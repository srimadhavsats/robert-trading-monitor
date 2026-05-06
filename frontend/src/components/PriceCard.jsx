import React, { useState, useEffect } from 'react';

const PriceCard = () => {
    const [data, setData] = useState(null);
    const [connected, setConnected] = useState(false);

    useEffect(() => {
        // Dynamic URL Logic:
        // Detects the current domain and switches the port from 5173 to 8000
        const currentHost = window.location.host;
        const backendHost = currentHost.replace('5173', '8000');
        const protocol = window.location.protocol === 'https:' ? 'wss' : 'ws';
        const wsUrl = `${protocol}://${backendHost}/ws/price/BTC-USDT`;

        console.log("Attempting connection to:", wsUrl);
        const socket = new WebSocket(wsUrl);

        socket.onopen = () => {
            setConnected(true);
            console.log("✅ WebSocket Connected");
        };

        socket.onmessage = (event) => {
            const incomingData = JSON.parse(event.data);
            setData(incomingData);
        };

        socket.onclose = (event) => {
            setConnected(false);
            console.log("❌ WebSocket Disconnected:", event.reason);
        };

        socket.onerror = (err) => {
            console.error("⚠️ WebSocket Error observed:", err);
        };

        return () => socket.close();
    }, []);

    // Loader state
    if (!data) return (
        <div className="p-6 border border-neutral-800 rounded-2xl bg-neutral-900/40 w-80 animate-pulse">
            <p className="text-neutral-500 font-mono text-xs uppercase">Initializing Stream...</p>
        </div>
    );

    return (
        <div className="p-6 border border-neutral-800 rounded-2xl bg-neutral-900/40 backdrop-blur-md w-80 shadow-2xl">
            <h3 className="text-neutral-500 text-xs font-bold uppercase tracking-widest mb-1">{data.symbol}</h3>
            <h2 className="text-4xl font-black text-emerald-400 tabular-nums mb-3 tracking-tighter italic">
                ${data.price.toLocaleString(undefined, { minimumFractionDigits: 2 })}
            </h2>
            <div className="flex items-center gap-2 mb-4">
                <span className={`h-2 w-2 rounded-full ${connected ? 'bg-emerald-500 animate-pulse' : 'bg-red-500'}`}></span>
                <span className="text-xs font-bold text-neutral-300 uppercase tracking-tighter">
                    {connected ? 'Live Stream' : 'Disconnected'}
                </span>
            </div>
            <div className="grid grid-cols-2 gap-2 pt-4 border-t border-neutral-800/50">
                <div>
                    <p className="text-[10px] text-neutral-500 uppercase font-bold">24h High</p>
                    <p className="text-sm font-mono text-neutral-200">${data.high?.toLocaleString()}</p>
                </div>
                <div>
                    <p className="text-[10px] text-neutral-500 uppercase font-bold">24h Low</p>
                    <p className="text-sm font-mono text-neutral-200">${data.low?.toLocaleString()}</p>
                </div>
            </div>
        </div>
    );
};

export default PriceCard;