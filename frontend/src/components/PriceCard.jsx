import React, { useState, useEffect } from 'react';
import axios from 'axios';

/**
 * PriceCard Component
 * Fetches and displays real-time market data from the FastAPI backend.
 */
const PriceCard = () => {
    const [data, setData] = useState(null);
    const [error, setError] = useState(null);

    // Function to fetch data from the backend API
    const fetchPrice = async () => {
        try {
            // Local/cloud backend URL
            // const response = await axios.get('/api/v1/sentinel/price');
            const response = await axios.get('https://cautious-zebra-64pr447qrq525wxw-8000.app.github.dev/api/v1/sentinel/price');
            setData(response.data);
            setError(null);
        } catch (err) {
            setError('Connection to Backend Failed');
        }
    };

    // Establishes a 1-second polling interval for real-time updates
    useEffect(() => {
        fetchPrice();
        const interval = setInterval(fetchPrice, 1000);
        return () => clearInterval(interval);
    }, []);

    if (error) return <div style={{ color: 'red' }}>{error}</div>;
    if (!data) return <div>Initializing Sentinel Data...</div>;

    return (
        <div style={{
            padding: '20px',
            border: '1px solid #333',
            borderRadius: '8px',
            backgroundColor: '#111',
            color: '#fff',
            width: '300px'
        }}>
            <h3>{data.symbol}</h3>
            <h2 style={{ color: data.status === 'LIVE' ? '#00ff00' : '#ffaa00' }}>
                ${data.price.toLocaleString()}
            </h2>
            <p>Status: <strong>{data.status}</strong></p>
            <div style={{ fontSize: '0.8rem', opacity: 0.7 }}>
                <p>24h High: ${data.high}</p>
                <p>24h Low: ${data.low}</p>
            </div>
        </div>
    );
};

export default PriceCard;