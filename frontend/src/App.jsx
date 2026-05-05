import PriceCard from './components/PriceCard';

/**
 * Main Application Shell
 * Acts as the container for all modular trading monitor components.
 */
function App() {
  return (
    <div style={{ backgroundColor: '#000', minHeight: '100vh', padding: '40px', color: '#eee' }}>
      <h1>Sats Trading Monitor v4.0</h1>
      <hr style={{ borderColor: '#333' }} />
      <div style={{ marginTop: '20px' }}>
        <PriceCard/>
      </div>
    </div>
  );
}

export default App;