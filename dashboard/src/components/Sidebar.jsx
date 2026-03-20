import React from 'react';
import { LayoutDashboard, Users, ChevronRight } from 'lucide-react';
import './Sidebar.css';

export default function Sidebar({ activeView, setActiveView, competitors, selectedCompetitor, setSelectedCompetitor }) {
  return (
    <aside className="sidebar glass-panel">
      <div className="sidebar-header">
        <div className="logo-box">EdRAM</div>
        <h2>Intelligence 2026</h2>
      </div>

      <nav className="sidebar-nav">
        <div className="nav-group">
          <p className="nav-label">Views</p>
          <button 
            className={`nav-btn ${activeView === 'consensus' ? 'active' : ''}`}
            onClick={() => setActiveView('consensus')}
          >
            <LayoutDashboard size={16} />
            <span>Consensus</span>
          </button>
          <button 
            className={`nav-btn ${activeView === 'comparison' ? 'active' : ''}`}
            onClick={() => setActiveView('comparison')}
          >
            <Users size={16} />
            <span>Comparison</span>
          </button>
        </div>

        {activeView === 'comparison' && (
          <div className="nav-group animate-fade-in fade-delay">
            <p className="nav-label mt-2">Competitors</p>
            <div className="competitor-list">
              {competitors.map(comp => (
                <button 
                  key={comp.manager}
                  className={`competitor-btn ${selectedCompetitor === comp.manager ? 'active' : ''}`}
                  onClick={() => setSelectedCompetitor(comp.manager)}
                >
                  <span className="comp-name">{comp.manager}</span>
                  <ChevronRight size={14} className="comp-arrow" />
                </button>
              ))}
            </div>
          </div>
        )}
      </nav>
    </aside>
  );
}
