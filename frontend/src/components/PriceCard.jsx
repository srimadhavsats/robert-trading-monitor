import React, { useState, useEffect, useRef } from 'react';

const lineCommand = (point, i, a) => {
    const [x, y] = point;
    if (i === 0) return `M ${x},${y}`;
    const [px, py] = a[i - 1];
    const cpx1 = px + (x - px) * 0.5;
    const cpy1 = py;
    const cpx2 = x - (x - px) * 0.5;
    const cpy2 = y;
    return `C ${cpx1},${cpy1} ${cpx2},${cpy2} ${x},${y}`;
};

const PriceCard = () => {
    const [selectedSymbol, setSelectedSymbol] = useState('BTC-USDT');
    const [data, setData] = useState(null);
    const [connected, setConnected] = useState(false);
    const [history, setHistory] = useState([]);
    const [latency, setLatency] = useState(0);
    const [flashSide, setFlashSide] = useState(null); // 'buy', 'sell', or null
    const socketRef = useRef(null);
    const maxTicks = 40;

    useEffect(() => {
        const currentHost = window.location.host;
        const backendHost = currentHost.replace('5173', '8000');
        const protocol = window.location.protocol === 'https:' ? 'wss' : 'ws';
        const wsUrl = `${protocol}://${backendHost}/ws/price/${selectedSymbol}`;

        const connect = () => {
            if (socketRef.current && socketRef.current.readyState !== WebSocket.CLOSED) return;
            socketRef.current = new WebSocket(wsUrl);
            socketRef.current.onopen = () => setConnected(true);
            socketRef.current.onmessage = (event) => {
                const incomingData = JSON.parse(event.data);
                if (incomingData.timestamp) setLatency(Date.now() - incomingData.timestamp);
                
                // --- TRIGGER FLASH LOGIC ---
                if (incomingData.trades && incomingData.trades.length > 0) {
                    const leadTrade = incomingData.trades[0];
                    // Trigger a flash for any trade hitting our Whale Tape
                    setFlashSide(leadTrade.side);
                    setTimeout(() => setFlashSide(null), 1000); // Pulse lasts 1 second
                }

                setData(incomingData);
                setHistory((prev) => [...prev, incomingData.price].slice(-maxTicks));
            };
            socketRef.current.onclose = () => {
                setConnected(false);
                setTimeout(connect, 3000);
            };
        };

        connect();
        return () => {
            if (socketRef.current) socketRef.current.close();
            setData(null);
            setHistory([]);
        };
    }, [selectedSymbol]);

    if (!data || history.length < 2) return (
        <div className="p-6 border border-neutral-800 rounded-2xl bg-neutral-900/40 w-96 animate-pulse flex flex-col justify-center items-center h-80">
            <p className="text-neutral-500 font-mono text-[10px] uppercase tracking-widest text-center">Uplink: {selectedSymbol}</p>
        </div>
    );

    const minPrice = Math.min(...history);
    const maxPrice = Math.max(...history);
    const priceRange = (maxPrice - minPrice) * 1.4 || 1;
    const chartMin = minPrice - (priceRange * 0.2);
    const prevPrice = history[history.length - 2];
    const isDropping = data.price < prevPrice;
    const velocityColor = isDropping ? '#fb923c' : '#10b981';

    const getPlotY = (price) => 128 - ((price - chartMin) / priceRange) * 128;
    const points = history.map((p, i) => [(i / (maxTicks - 1)) * 384, getPlotY(p)]);
    const dAttr = points.map((point, i, a) => lineCommand(point, i, a)).join(' ');

    // Dynamic Flash Classes
    const flashClasses = flashSide === 'buy' 
        ? 'ring-2 ring-emerald-500/50 shadow-[0_0_30px_rgba(16,185,129,0.3)]' 
        : flashSide === 'sell' 
        ? 'ring-2 ring-orange-500/50 shadow-[0_0_30px_rgba(249,115,22,0.3)]' 
        : 'border-neutral-800';

    return (
        <div className={`p-6 border rounded-2xl bg-neutral-900/95 backdrop-blur-2xl w-96 relative overflow-hidden transition-all duration-300 ${flashClasses}`}>
            
            {/* ASSET SELECTOR */}
            <div className="absolute left-6 top-6 flex gap-2 z-50">
                {['BTC-USDT', 'ETH-USDT'].map((sym) => (
                    <button
                        key={sym}
                        onClick={() => setSelectedSymbol(sym)}
                        className={`text-[8px] font-black px-2 py-1 rounded border transition-all 
                        ${selectedSymbol === sym ? 'bg-neutral-100 text-black border-neutral-100' : 'bg-transparent text-neutral-500 border-neutral-800 hover:border-neutral-600'}`}
                    >
                        {sym.split('-')[0]}
                    </button>
                ))}
            </div>

            {/* WHALE TAPE */}
            <div className="absolute right-2 top-24 bottom-14 w-24 flex flex-col gap-1.5 overflow-hidden pointer-events-none z-50">
                {data.trades?.slice(0, 5).map((trade, i) => (
                    <div key={i} className={`text-[7px] font-black py-1 px-2 rounded bg-black/80 backdrop-blur-md border-r-2 flex justify-between items-center animate-in fade-in slide-in-from-right-4 duration-500
                        ${trade.side === 'sell' ? 'border-orange-500 text-orange-400' : 'border-emerald-500 text-emerald-400'}`}>
                        <span>{trade.side.toUpperCase()}</span>
                        <span className="font-mono">{trade.amount.toFixed(2)}</span>
                    </div>
                ))}
            </div>

            {/* HEADER */}
            <div className="relative z-30 mb-6">
                <div className="flex justify-between items-center mb-1">
                    <h3 className="text-neutral-500 text-[9px] font-black uppercase tracking-[0.3em] pl-24">{data.symbol} / PERP</h3>
                    <div className="flex items-center gap-2">
                        <span className="text-neutral-600 font-mono text-[9px] font-bold">{latency}ms</span>
                        <div className={`px-1.5 py-0.5 rounded-[4px] text-[8px] font-black uppercase ${connected ? 'bg-emerald-500/10 text-emerald-400' : 'bg-red-500/10 text-red-400'}`}>
                            {connected ? '● Live' : '○ Offline'}
                        </div>
                    </div>
                </div>
                <h2 className="text-5xl font-black tabular-nums tracking-tighter italic transition-colors duration-1000" style={{ color: velocityColor }}>
                    ${data.price.toLocaleString(undefined, { minimumFractionDigits: 2 })}
                </h2>
            </div>

            {/* VISUALIZATION BOX */}
            <div className="relative h-32 w-full bg-black/60 rounded-xl border border-neutral-800/40 overflow-hidden mb-5">
                <div className="absolute top-0 left-0 w-full h-1 bg-neutral-800 z-50 flex">
                    <div className="h-full bg-emerald-500 transition-all duration-1000 ease-linear shadow-[0_0_8px_rgba(16,185,129,0.4)]" style={{ width: `${data.imbalance}%` }} />
                    <div className="h-full bg-orange-500 transition-all duration-1000 ease-linear shadow-[0_0_8px_rgba(249,115,22,0.4)]" style={{ width: `${100 - data.imbalance}%` }} />
                </div>

                <div className="absolute inset-0 pointer-events-none">
                    {data.walls?.map((wall, index) => {
                        const yPos = getPlotY(wall.price);
                        if (yPos < 0 || yPos > 128) return null;
                        return (
                            <div key={index} className="absolute w-full border-t transition-all duration-1000 ease-linear"
                                style={{ 
                                    top: `${yPos}px`,
                                    borderColor: `rgba(251, 146, 60, ${Math.min(wall.volume / 2, 0.4)})`,
                                    boxShadow: `0 0 12px rgba(251, 146, 60, ${Math.min(wall.volume / 4, 0.2)})`
                                }}
                            />
                        );
                    })}
                </div>

                <svg className="absolute inset-0 w-full h-full" viewBox="0 0 384 128" preserveAspectRatio="none">
                    <defs>
                        <linearGradient id="liquidGradient" x1="0" y1="0" x2="0" y2="1">
                            <stop offset="0%" stopColor={velocityColor} stopOpacity="0.4" />
                            <stop offset="100%" stopColor={velocityColor} stopOpacity="0" />
                        </linearGradient>
                    </defs>
                    <path d={`${dAttr} L 384,128 L 0,128 Z`} fill="url(#liquidGradient)" className="transition-all duration-1000 ease-linear" />
                    <path d={dAttr} fill="none" stroke={velocityColor} strokeWidth="3" strokeLinecap="round" className="transition-all duration-1000 ease-linear" />
                </svg>

                <div className="absolute right-1 w-2.5 h-2.5 rounded-full transition-all duration-1000 ease-linear z-40"
                    style={{ top: `${getPlotY(data.price) - 5}px`, backgroundColor: velocityColor, boxShadow: `0 0 15px ${velocityColor}` }}
                />
            </div>

            {/* FOOTER */}
            <div className="flex justify-between items-end border-t border-neutral-800 pt-4">
                <div className="flex flex-col gap-1">
                    <p className="text-neutral-600 text-[8px] font-black uppercase tracking-widest">Network Friction</p>
                    <div className="flex gap-3">
                        <div className="flex flex-col">
                            <span className="text-[7px] text-neutral-500 uppercase font-bold tracking-tighter">Fastest</span>
                            <span className={`text-[11px] font-mono font-black ${data.fees?.fastestFee > 100 ? 'text-orange-400' : 'text-emerald-400'}`}>
                                {data.fees?.fastestFee || '--'} <span className="text-[7px] opacity-60">sat/vB</span>
                            </span>
                        </div>
                        <div className="flex flex-col border-l border-neutral-800 pl-3">
                            <span className="text-[7px] text-neutral-500 uppercase font-bold tracking-tighter">1 Hour</span>
                            <span className="text-[11px] font-mono font-black text-neutral-300">
                                {data.fees?.hourFee || '--'} <span className="text-[7px] opacity-60">sat/vB</span>
                            </span>
                        </div>
                    </div>
                </div>
                <div className="text-right">
                    <p className={`text-[10px] font-black uppercase italic tracking-tighter transition-colors duration-1000`} style={{ color: velocityColor }}>
                        {isDropping ? 'High-Gravity Rejection' : 'Impulse Momentum'}
                    </p>
                </div>
            </div>
        </div>
    );
};

export default PriceCard;