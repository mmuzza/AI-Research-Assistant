import React, { useState } from "react";
import PaperCard from "./PaperCard";
import KnowledgeGraph from "./KnowledgeGraph";
import "./ReportTabs.css";

const TABS = [
  { id: "papers",      label: "Papers",      icon: "⬡" },
  { id: "summary",     label: "Summary",     icon: "◈" },
  { id: "gaps",        label: "Gaps",        icon: "◎" },
  { id: "graph",       label: "Graph",       icon: "◇" },
  { id: "experiments", label: "Experiments", icon: "⊞" },
  { id: "comparison",  label: "Comparison",  icon: "≋" },
];

export default function ReportTabs({ data }) {
  const [active, setActive] = useState("papers");

  return (
    <div className="report-tabs-wrapper">
      {/* Tab bar */}
      <div className="tab-bar">
        {TABS.map((tab) => (
          <button
            key={tab.id}
            className={`tab-btn ${active === tab.id ? "tab-btn--active" : ""}`}
            onClick={() => setActive(tab.id)}
          >
            <span className="tab-icon">{tab.icon}</span>
            {tab.label}
          </button>
        ))}
      </div>

      {/* Tab content */}
      <div className="tab-content">
        {active === "papers"      && <PapersTab      data={data} />}
        {active === "summary"     && <SummaryTab     data={data} />}
        {active === "gaps"        && <GapsTab        data={data} />}
        {active === "graph"       && <GraphTab       data={data} />}
        {active === "experiments" && <ExperimentsTab data={data} />}
        {active === "comparison"  && <ComparisonTab  data={data} />}
      </div>
    </div>
  );
}


function PapersTab({ data }) {
  const papers = data.retrievedPapers || [];
  return (
    <div className="tab-pane">
      <div className="tab-pane-header">
        <h3 className="tab-pane-title">Retrieved Papers</h3>
        <span className="tab-pane-count">{papers.length} papers</span>
      </div>
      {papers.map((p, i) => <PaperCard key={p.paper_id || i} paper={p} index={i} />)}
    </div>
  );
}


function SummaryTab({ data }) {
  const [openId, setOpenId] = useState(null);

  return (
    <div className="tab-pane">
      {data.globalSummary && (
        <div className="global-summary-block">
          <div className="block-label">Overall Summary</div>
          <p className="global-summary-text">{data.globalSummary}</p>
        </div>
      )}
      {data.paperSummaries?.length > 0 && (
        <>
          <div className="block-label" style={{ marginTop: 28 }}>Per-Paper Summaries</div>
          {data.paperSummaries.map((p, i) => (
            <div key={p.paper_id || i} className="summary-accordion">
              <button
                className="accordion-trigger"
                onClick={() => setOpenId(openId === p.paper_id ? null : p.paper_id)}
              >
                <span className="accordion-index">{String(i + 1).padStart(2, "0")}</span>
                <span className="accordion-title">{p.title}</span>
                <span className={`accordion-chevron ${openId === p.paper_id ? "accordion-chevron--open" : ""}`}>
                  ›
                </span>
              </button>
              {openId === p.paper_id && (
                <div className="accordion-body">
                  {p.authors && (
                    <p className="accordion-meta">
                      {Array.isArray(p.authors) ? p.authors.slice(0, 3).join(", ") : p.authors}
                    </p>
                  )}
                  <p className="accordion-summary">{p.summary}</p>
                </div>
              )}
            </div>
          ))}
        </>
      )}
    </div>
  );
}


function GapsTab({ data }) {
  const gaps = data.researchGaps;
  if (!gaps) return <EmptyState label="No gap data available." />;

  const lines = (gaps.insights || "")
    .split("\n")
    .filter((l) => l.trim().length > 0);

  return (
    <div className="tab-pane">
      {lines.length > 0 && (
        <>
          <div className="block-label">Analysis & Insights</div>
          <div className="insights-block">
            {lines.map((line, i) => (
              <p key={i} className="insight-line">{line}</p>
            ))}
          </div>
        </>
      )}
    </div>
  );
}


function GraphTab({ data }) {
  if (!data.graph?.nodes?.length) return <EmptyState label="No graph data available." />;
  return (
    <div className="tab-pane tab-pane--graph">
      <div className="block-label">Knowledge Graph</div>
      <p className="block-subtitle">
        {data.graph.nodes.length} entities · {data.graph.edges?.length || 0} relationships
      </p>
      <div className="graph-container">
        <KnowledgeGraph graph={data.graph} />
      </div>
    </div>
  );
}


const DIFFICULTY_COLOR = { easy: "#4ade80", medium: "#f0a500", hard: "#e05c5c" };

function ExperimentsTab({ data }) {
  const ideas = data.experiments?.ideas || [];
  if (!ideas.length) return <EmptyState label="No experiment ideas available." />;

  return (
    <div className="tab-pane">
      <div className="block-label">{ideas.length} Proposed Experiments</div>
      <div className="experiment-grid">
        {ideas.map((idea, i) => (
          <div key={i} className="experiment-card">
            <div className="experiment-card-header">
              <span className="experiment-index">{String(i + 1).padStart(2, "0")}</span>
              <span
                className="difficulty-badge"
                style={{ color: DIFFICULTY_COLOR[idea.difficulty?.toLowerCase()] || "var(--text-muted)" }}
              >
                {idea.difficulty}
              </span>
            </div>
            <h4 className="experiment-title">{idea.title}</h4>
            <p className="experiment-desc">{idea.description}</p>
            <div className="experiment-detail">
              <span className="detail-label">Method</span>
              <p className="detail-text">{idea.method}</p>
            </div>
            <div className="experiment-detail">
              <span className="detail-label">Expected Outcome</span>
              <p className="detail-text">{idea.expected_outcome}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}


function ComparisonTab({ data }) {
  const raw = data.comparison || "";
  if (!raw) return <EmptyState label="No comparison available." />;


  const sections = raw.split(/\n(?=\*\*|##|\d+\.)/).filter(Boolean);

  return (
    <div className="tab-pane">
      <div className="block-label">Comparison Analysis</div>
      <div className="comparison-body">
        {sections.map((block, i) => {
          const lines = block.split("\n").filter((l) => l.trim());
          const headerMatch = lines[0]?.match(/^[*#\d.\s]+(.+?)[*#\s]*$/);
          const header = headerMatch?.[1] || lines[0];
          const body = lines.slice(1).join("\n");

          return (
            <div key={i} className="comparison-section">
              {header && <h4 className="comparison-section-title">{header.replace(/\*/g, "")}</h4>}
              {body && <p className="comparison-section-body">{body.replace(/\*\*/g, "")}</p>}
            </div>
          );
        })}
      </div>
    </div>
  );
}


function EmptyState({ label }) {
  return (
    <div className="tab-pane">
      <p className="empty-state">{label}</p>
    </div>
  );
}