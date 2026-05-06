import React, { useState, useEffect } from 'react';
import axios from 'axios';

const PriceCard = () => {
    const [data, setData] = useState(null);
    const [error, setError] = useState(null);

    const fetchPrice = async () => {
        try {
            // Ensure this URL matches your active Codespace/Local port
            const response = await axios.get('http://localhost:8000/api/v1/sentinel/price');
            setData(response.data);
            setError(null);
        } catch (err) {
            setError('Backend Offline');
        }
    };

    useEffect(() => {
        fetchPrice();
        const interval = setInterval(fetchPrice, 1000);
        return () => clearInterval(interval);
    }, []);

    if (error) return <div className="text-red-500 font-mono text-sm uppercase">{error}</div>;
    if (!data) return <div className="text-neutral-500 animate-pulse font-mono">Connecting...</div>;

    return (
        <div className="p-6 border border-neutral-800 rounded-2xl bg-neutral-900/40 backdrop-blur-md w-80 shadow-2xl">
            <h3 className="text-neutral-500 text-xs font-bold uppercase tracking-widest mb-1">
                {data.symbol}
            </h3>
            <h2 className="text-4xl font-black text-emerald-400 tabular-nums mb-3 tracking-tighter">
                ${data.price.toLocaleString()}
            </h2>
            <div className="flex items-center gap-2 mb-4">
                <span className="relative flex h-2 w-2">
                    <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                    <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
                </span>
                <span className="text-xs font-bold text-neutral-300 uppercase tracking-tighter">
                    Status: {data.status}
                </span>
            </div>
            <div className="grid grid-cols-2 gap-2 pt-4 border-t border-neutral-800/50">
                <div>
                    <p className="text-[10px] text-neutral-500 uppercase font-bold">24h High</p>
                    <p className="text-sm font-mono text-neutral-200">${data.high.toLocaleString()}</p>
                </div>
                <div>
                    <p className="text-[10px] text-neutral-500 uppercase font-bold">24h Low</p>
                    <p className="text-sm font-mono text-neutral-200">${data.low.toLocaleString()}</p>
                </div>
            </div>
        </div>
    );
};

export default PriceCard;