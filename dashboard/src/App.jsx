import React, { useState } from 'react';
import { useData } from './hooks/useData';
import Sidebar from './components/Sidebar';
import ComparisonView from './components/ComparisonView';
import ConsensusView from './components/ConsensusView';
import EvidencePanel from './components/EvidencePanel';
import { Loader2 } from 'lucide-react';
import './App.css';

export default function App() {
  const { data, loading, error } = useData();
  const [activeView, setActiveView] = useState('consensus'); // 'comparison' | 'consensus'
  const [selectedCompetitor, setSelectedCompetitor] = useState(null);
  const [evidenceData, setEvidenceData] = useState(null);

  if (loading) {
    return (
      <div className="loading-screen">
        <Loader2 className="loading-icon" size={28} />
        <span>Loading EdRAM Intelligence Database...</span>
      </div>
    );
  }

  if (error) {
    return <div style={{ color: 'var(--status-negative-text)', padding: '2rem' }}>Error loading data: {error.message}</div>;
  }

  const edramRow = data.find(r => r.manager === 'EdRAM');
  const competitors = data.filter(r => r.manager !== 'EdRAM' && r.manager !== 'Benchmark');
  
  if (!selectedCompetitor && competitors.length > 0) {
    setSelectedCompetitor(competitors[0].manager);
  }

  const activeCompetitorRow = competitors.find(r => r.manager === selectedCompetitor);

  return (
    <div className="app-container animate-fade-in">
      <Sidebar 
        activeView={activeView} 
        setActiveView={setActiveView} 
        competitors={competitors}
        selectedCompetitor={selectedCompetitor}
        setSelectedCompetitor={setSelectedCompetitor}
      />
      
      <main className="main-content">
        <header className="main-header">
          <h1>
            {activeView === 'comparison' ? 'Asset Manager Comparison' : 'EdRAM vs Consensus'}
          </h1>
          <p>
            {activeView === 'comparison' 
              ? "Compare EdRAM's 2026 outlook against individual competitors side-by-side." 
              : "Analyze where EdRAM diverges or aligns with the broader market consensus."}
          </p>
        </header>

        {activeView === 'comparison' ? (
          <ComparisonView 
            edram={edramRow} 
            competitor={activeCompetitorRow} 
            onShowEvidence={setEvidenceData} 
          />
        ) : (
          <ConsensusView 
            edram={edramRow} 
            competitors={competitors} 
            onShowEvidence={setEvidenceData} 
          />
        )}
      </main>

      <EvidencePanel data={evidenceData} onClose={() => setEvidenceData(null)} />
    </div>
  );
}
