import React, { useState } from "react";
import SearchBar from "./components/SearchBar";
import PipelinePanel from "./components/PipelinePanel";
import ReportTabs from "./components/ReportTabs";
import {
  retrievePapers,
  fetchGaps,
  fetchGraph,
  fetchExperiments,
  fetchComparison,
} from "./api/api";
import "./App.css";

const INITIAL_STEPS = [
  { id: "retrieve",    label: "Retrieval & Summarization", status: "idle", stat: null },
  { id: "gaps",        label: "Research Gap Analysis",     status: "idle", stat: null },
  { id: "graph",       label: "Knowledge Graph",           status: "idle", stat: null },
  { id: "experiments", label: "Experiment Ideas",          status: "idle", stat: null },
  { id: "compare",     label: "Comparison Analysis",       status: "idle", stat: null },
];

const setStepStatus = (steps, id, status, stat = null) =>
  steps.map((s) => (s.id === id ? { ...s, status, stat: stat ?? s.stat } : s));

export default function App() {
  const [phase, setPhase] = useState("idle"); // idle | pipeline | complete
  const [steps, setSteps] = useState(INITIAL_STEPS);
  const [error, setError] = useState(null);
  // const [lastQuery, setLastQuery] = useState("");

  const [data, setData] = useState({
    retrievedPapers: [],
    paperSummaries: [],
    globalSummary: "",
    researchGaps: null,
    graph: null,
    experiments: null,
    comparison: null,
  });

  const updateStep = (id, status, stat = null) =>
    setSteps((prev) => setStepStatus(prev, id, status, stat));

  const handleSearch = async (query) => {
    // setLastQuery(query);
    setError(null);
    setPhase("pipeline");
    setSteps(INITIAL_STEPS);
    setData({
      retrievedPapers: [], paperSummaries: [], globalSummary: "",
      researchGaps: null, graph: null, experiments: null, comparison: null,
    });

    let paperSummaries = [];
    let researchGaps   = null;

    try {
      // Step 1: Retrieve + Summarize
      updateStep("retrieve", "active");
      const r1 = await retrievePapers(query);
      paperSummaries = r1.paper_summaries || [];
      setData((d) => ({
        ...d,
        retrievedPapers: r1.retrieved_papers || [],
        paperSummaries,
        globalSummary: r1.global_summary || "",
      }));
      updateStep("retrieve", "done", `${(r1.retrieved_papers || []).length} papers · ${paperSummaries.length} summaries`);

      if (!paperSummaries.length) {
        setError("No papers found. Try a different query.");
        setPhase("complete");
        return;
      }

      // Step 2: Gaps
      updateStep("gaps", "active");
      const r2 = await fetchGaps(paperSummaries);
      researchGaps = r2;
      setData((d) => ({ ...d, researchGaps: r2 }));
      const gapCount = (r2.basic_gaps || []).length;
      updateStep("gaps", "done", `${gapCount} gap${gapCount !== 1 ? "s" : ""} identified`);

      // Step 3: Graph
      updateStep("graph", "active");
      const r3 = await fetchGraph(paperSummaries);
      setData((d) => ({ ...d, graph: r3 }));
      updateStep("graph", "done", `${(r3.nodes || []).length} entities · ${(r3.edges || []).length} edges`);

      // Step 4: Experiments
      updateStep("experiments", "active");
      const r4 = await fetchExperiments(paperSummaries, researchGaps);
      setData((d) => ({ ...d, experiments: r4 }));
      const ideaCount = (r4.ideas || []).length;
      updateStep("experiments", "done", `${ideaCount} idea${ideaCount !== 1 ? "s" : ""} generated`);

      // Step 5: Compare
      updateStep("compare", "active");
      const r5 = await fetchComparison(paperSummaries);
      setData((d) => ({ ...d, comparison: r5.comparison || "" }));
      updateStep("compare", "done", "Analysis complete");

    } catch (err) {
      console.error("Pipeline error:", err);
      setError("Something went wrong. Make sure the backend is running.");
    }

    setPhase("complete");
  };

  const isSearching = phase === "pipeline";

  return (
    <div className="app-wrapper">
      <header className="app-header">
        <p className="app-eyebrow"><span /> AI Research Assistant <span /></p>
        <h1 className="app-title">
          Explore <em>arXiv</em> research,<br />Intelligently.
        </h1>
        <p className="app-subtitle">
          Five specialized agents retrieve, summarize, analyze, and visualize the latest research — automatically.
        </p>
      </header>

      <main className="app-main">
        <SearchBar onSearch={handleSearch} loading={isSearching} />

        {phase !== "idle" && (
          <PipelinePanel steps={steps} collapsed={phase === "complete"} />
        )}

        {error && <div className="status-error">⚠ {error}</div>}

        {phase === "complete" && !error && (
          <ReportTabs data={data} />
        )}

        {phase === "idle" && (
          <div className="idle-state">
            <div className="idle-agent-grid">
              {[
                { icon: "⬡", label: "Retrieval",      desc: "Fetches & embeds arXiv papers" },
                { icon: "◈", label: "Summarizer",     desc: "Extracts key contributions" },
                { icon: "◎", label: "Gap Analyst",    desc: "Finds unexplored directions" },
                { icon: "◇", label: "Knowledge Graph",desc: "Maps entity relationships" },
                { icon: "⊞", label: "Experiments",    desc: "Proposes novel research ideas" },
                { icon: "≋", label: "Comparison",     desc: "Benchmarks approaches" },
              ].map((a) => (
                <div key={a.label} className="idle-agent-card">
                  <span className="idle-agent-icon">{a.icon}</span>
                  <span className="idle-agent-label">{a.label}</span>
                  <span className="idle-agent-desc">{a.desc}</span>
                </div>
              ))}
            </div>
          </div>
        )}
      </main>

      <footer className="app-footer">
        AI Research Assistant · arXiv &nbsp;&mdash;&nbsp; <em>Muhammad Muzzammil</em>
      </footer>
    </div>
  );
}