import PriceCard from './components/PriceCard';

function App() {
  return (
    // 'bg-neutral-950' and 'text-white' are Tailwind classes
    <div className="min-h-screen bg-neutral-950 p-10 text-white font-sans">
      <header className="mb-10 border-b border-neutral-800 pb-5">
        <h1 className="text-4xl font-black tracking-tighter text-emerald-400 italic">
  SATS SENTINEL v4.1
</h1>
        <p className="mt-2 text-neutral-400 text-sm uppercase tracking-widest">
          Institutional Liquidity Monitor
        </p>
      </header>

      <main className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <PriceCard />
      </main>
    </div>
  );
}

export default App;