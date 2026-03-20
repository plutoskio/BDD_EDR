import React from 'react';
import { X, FileText } from 'lucide-react';
import './EvidencePanel.css';

export default function EvidencePanel({ data, onClose }) {
  if (!data) return null;

  const { metric, edram, competitor, compName } = data;

  return (
    <>
      <div className="evidence-overlay animate-fade-in" onClick={onClose} />
      <div className="evidence-panel glass-panel animate-slide-in">
        <header className="evidence-header">
          <div className="evidence-title">
            <FileText size={18} className="text-accent" />
            <h3>Evidence & Source</h3>
          </div>
          <button className="close-btn" onClick={onClose}>
            <X size={20} />
          </button>
        </header>

        <div className="evidence-content">
          <h4 className="metric-name">{metric}</h4>

          <div className="source-card">
            <div className="source-brand border-edram">EdRAM (Benchmark)</div>
            <div className="source-body">
              {edram.status === 'ND' ? (
                <p className="nd-text">Not Disclosed explicitly.</p>
              ) : (
                <>
                  <p className="source-quote">"{edram.raw_wording || edram.wording}"</p>
                  <p className="source-why">{edram.why}</p>
                  <div className="source-meta">
                    <span className="page-badge">Page {edram.page}</span>
                    <span className="doc-name">{edram.source_file || 'EDRAM - Outlook 2026.pdf'}</span>
                  </div>
                </>
              )}
            </div>
          </div>

          {competitor && (
            <div className="source-card">
              <div className="source-brand border-comp">{compName}</div>
              <div className="source-body">
                {competitor.status === 'ND' ? (
                  <p className="nd-text">Not Disclosed</p>
                ) : (
                  <>
                    <p className="source-quote">"{competitor.raw_wording || competitor.wording}"</p>
                    <p className="source-why">{competitor.why}</p>
                    <div className="source-meta">
                      <span className="page-badge">Page {competitor.page}</span>
                      <span className="doc-name">{competitor.source_file}</span>
                    </div>
                  </>
                )}
              </div>
            </div>
          )}
          
        </div>
      </div>
    </>
  );
}
