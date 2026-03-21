// import React, { useState } from "react";
// import SearchBar from "./components/SearchBar";
// import PaperCard from "./components/PaperCard";
// import { searchPapers } from "./api/api";
// import "./App.css";

// export default function App() {
//   const [retrievedPapers, setRetrievedPapers] = useState([]);
//   const [paperSummaries, setPaperSummaries] = useState([]);
//   const [globalSummary, setGlobalSummary] = useState("");
//   const [loading, setLoading] = useState(false);
//   const [summarizing, setSummarizing] = useState(false);
//   const [error, setError] = useState(null);
//   const [hasSearched, setHasSearched] = useState(false);
//   const [lastQuery, setLastQuery] = useState("");

//   const handleSearch = async (query) => {
//     setLoading(true);
//     setError(null);
//     setHasSearched(true);
//     setLastQuery(query);

//     try {
//       const response = await searchPapers(query);

//       // Extract data from orchestrator response
//       const retrieved = Array.isArray(response?.retrieved_papers)
//         ? response.retrieved_papers
//         : [];
//       const summaries = Array.isArray(response?.paper_summaries)
//         ? response.paper_summaries
//         : [];
//       const globalSum = response?.summary || "";

//       // Show retrieved papers immediately
//       setRetrievedPapers(retrieved);
//       setPaperSummaries([]); // reset summaries while summarization happens
//       setGlobalSummary("");

//       // Show "summarizing" label if summaries not ready
//       setSummarizing(retrieved.length > 0 && summaries.length === 0);

//       // Once summaries are available, update state
//       if (summaries.length > 0) {
//         setPaperSummaries(summaries);
//         setGlobalSummary(globalSum);
//         setSummarizing(false);
//       }

//       console.log("API response:", response);
//     } catch (err) {
//       console.error("Error fetching papers:", err);
//       setError("Could not reach the server. Make sure the backend is running.");
//       setRetrievedPapers([]);
//       setPaperSummaries([]);
//       setGlobalSummary("");
//       setSummarizing(false);
//     }

//     setLoading(false);
//   };

//   return (
//     <div className="app-wrapper">
//       {/* ── Header ── */}
//       <header className="app-header">
//         <p className="app-eyebrow">
//           <span /> AI Research Assistant <span />
//         </p>
//         <h1 className="app-title">
//           Explore <em>arXiv</em> research,<br />intelligently.
//         </h1>
//         <p className="app-subtitle">
//           Ask a question in plain language. Our retrieval agent finds the most relevant papers for you.
//         </p>
//       </header>

//       {/* ── Main ── */}
//       <main className="app-main">
//         <SearchBar onSearch={handleSearch} loading={loading} />

//         {/* Loading */}
//         {loading && (
//           <div className="status-loading">
//             <div className="spinner" />
//             Searching arXiv papers…
//           </div>
//         )}

//         {/* Error */}
//         {error && !loading && (
//           <div className="status-error">⚠ {error}</div>
//         )}

//         {/* Retrieved Papers */}
//         {!loading && retrievedPapers.length > 0 && (
//           <>
//             <div className="results-header">
//               <span className="results-count">
//                 <strong>{retrievedPapers.length}</strong> paper{retrievedPapers.length !== 1 ? "s" : ""} found
//                 {lastQuery && <> for "{lastQuery}"</>}
//               </span>
//             </div>
//             <div className="results-list">
//               {retrievedPapers.map((paper, i) => (
//                 <PaperCard key={paper.paper_id || i} paper={paper} index={i} />
//               ))}
//             </div>
//           </>
//         )}

//         {/* Summarizing */}
//         {summarizing && (
//           <div className="status-loading">
//             <div className="spinner" />
//             Summarizing papers…
//           </div>
//         )}

//         {/* Paper Summaries */}
//         {!loading && paperSummaries.length > 0 && (
//           <>
//             <h2>Paper Summaries</h2>
//             <div className="results-list">
//               {paperSummaries.map((paper, i) => (
//                 <PaperCard key={paper.paper_id || i} paper={paper} index={i} showSummary />
//               ))}
//             </div>
//             <h2>Global Summary</h2>
//             <p className="global-summary">{globalSummary}</p>
//           </>
//         )}

//         {/* Empty */}
//         {!loading && hasSearched && retrievedPapers.length === 0 && !error && (
//           <p className="status-empty">
//             No papers found for "{lastQuery}" — try broadening your query.
//           </p>
//         )}
//       </main>

//       {/* ── Footer ── */}
//       <footer className="app-footer">
//         AI Research Assistant · arXiv &nbsp;&mdash;&nbsp; <em>Muhammad Muzzammil</em>
//       </footer>
//     </div>
//   );
// }











import React, { useState } from "react";
import SearchBar from "./components/SearchBar";
import PaperCard from "./components/PaperCard";
import { searchPapers } from "./api/api";
import "./App.css";

export default function App() {
  const [retrievedPapers, setRetrievedPapers] = useState([]);
  const [paperSummaries, setPaperSummaries] = useState([]);
  const [globalSummary, setGlobalSummary] = useState("");
  const [researchGaps, setResearchGaps] = useState(null);
  const [comparison, setComparison] = useState(null);
  const [loading, setLoading] = useState(false);
  const [summarizing, setSummarizing] = useState(false);
  const [error, setError] = useState(null);
  const [hasSearched, setHasSearched] = useState(false);
  const [lastQuery, setLastQuery] = useState("");

  const handleSearch = async (query) => {
    setLoading(true);
    setError(null);
    setHasSearched(true);
    setLastQuery(query);

    try {
      const response = await searchPapers(query);

      const retrieved = Array.isArray(response?.retrieved_papers)
        ? response.retrieved_papers
        : [];
      const summaries = Array.isArray(response?.paper_summaries)
        ? response.paper_summaries
        : [];
      const globalSum = response?.summary || "";
      const gaps = response?.research_gaps || null;
      const comp = response?.comparison || null;

      // Reset state while loading
      setRetrievedPapers(retrieved);
      setPaperSummaries([]);
      setGlobalSummary("");
      setResearchGaps(null);
      setComparison(null);

      // Show "summarizing" label if summaries not ready
      setSummarizing(retrieved.length > 0 && summaries.length === 0);

      // Once summaries are available, update state
      if (summaries.length > 0) {
        setPaperSummaries(summaries);
        setGlobalSummary(globalSum);
        setSummarizing(false);
      }

      // Set new agents' outputs
      if (gaps) setResearchGaps(gaps);
      if (comp) setComparison(comp);

      console.log("API response:", response);
    } catch (err) {
      console.error("Error fetching papers:", err);
      setError("Could not reach the server. Make sure the backend is running.");
      setRetrievedPapers([]);
      setPaperSummaries([]);
      setGlobalSummary("");
      setResearchGaps(null);
      setComparison(null);
      setSummarizing(false);
    }

    setLoading(false);
  };

  return (
    <div className="app-wrapper">
      <header className="app-header">
        <p className="app-eyebrow">
          <span /> AI Research Assistant <span />
        </p>
        <h1 className="app-title">
          Explore <em>arXiv</em> research,<br />intelligently.
        </h1>
        <p className="app-subtitle">
          Ask a question in plain language. Our retrieval agent finds the most relevant papers for you.
        </p>
      </header>

      <main className="app-main">
        <SearchBar onSearch={handleSearch} loading={loading} />

        {loading && (
          <div className="status-loading">
            <div className="spinner" />
            Searching arXiv papers…
          </div>
        )}

        {error && !loading && <div className="status-error">⚠ {error}</div>}

        {/* Retrieved Papers */}
        {!loading && retrievedPapers.length > 0 && (
          <>
            <div className="results-header">
              <span className="results-count">
                <strong>{retrievedPapers.length}</strong> paper{retrievedPapers.length !== 1 ? "s" : ""} found
                {lastQuery && <> for "{lastQuery}"</>}
              </span>
            </div>
            <div className="results-list">
              {retrievedPapers.map((paper, i) => (
                <PaperCard key={paper.paper_id || i} paper={paper} index={i} />
              ))}
            </div>
          </>
        )}

        {summarizing && (
          <div className="status-loading">
            <div className="spinner" />
            Summarizing papers…
          </div>
        )}

        {/* Paper Summaries */}
        {!loading && paperSummaries.length > 0 && (
          <>
            <h2>Paper Summaries</h2>
            <div className="results-list">
              {paperSummaries.map((paper, i) => (
                <PaperCard key={paper.paper_id || i} paper={paper} index={i} showSummary />
              ))}
            </div>
            <h2>Global Summary</h2>
            <p className="global-summary">{globalSummary}</p>
          </>
        )}

        {/* Research Gaps */}
        {!loading && researchGaps && (
          <div className="research-gaps">
            <h2>Research Gaps</h2>

            {researchGaps.basic_gaps && researchGaps.basic_gaps.length > 0 && (
              <>
                <h3>Basic Gaps:</h3>
                <ul>
                  {researchGaps.basic_gaps.map((gap, i) => (
                    <li key={i}>{gap}</li>
                  ))}
                </ul>
              </>
            )}

            {researchGaps.insights && (
              <>
                <h3>Insights:</h3>
                <ul>
                  {researchGaps.insights
                    .split("\n")
                    .filter((line) => line.trim() !== "")
                    .map((line, i) => (
                      <li key={i}>{line.trim()}</li>
                    ))}
                </ul>
              </>
            )}
          </div>
        )}

        {/* Comparison */}
        {!loading && comparison && (
          <div className="comparison">
            <h2>Comparison Insights</h2>
            <pre>{comparison}</pre>
          </div>
        )}

        {!loading && hasSearched && retrievedPapers.length === 0 && !error && (
          <p className="status-empty">
            No papers found for "{lastQuery}" — try broadening your query.
          </p>
        )}
      </main>

      <footer className="app-footer">
        AI Research Assistant · arXiv &nbsp;&mdash;&nbsp; <em>Muhammad Muzzammil</em>
      </footer>
    </div>
  );
}