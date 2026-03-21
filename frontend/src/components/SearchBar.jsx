import React, { useState, useRef } from "react";
import "./SearchBar.css";

export default function SearchBar({ onSearch, loading }) {
  const [query, setQuery] = useState("");
  const inputRef = useRef(null);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (query.trim() && !loading) onSearch(query.trim());
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter") handleSubmit(e);
  };

  const suggestions = [
    "transformer architectures",
    "diffusion models in medicine",
    "large language model alignment",
    "reinforcement learning robotics",
  ];

  return (
    <div className="searchbar-wrapper">
      <form className="searchbar-form" onSubmit={handleSubmit}>
        <div className="searchbar-icon">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none"
            stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <circle cx="11" cy="11" r="8" />
            <line x1="21" y1="21" x2="16.65" y2="16.65" />
          </svg>
        </div>
        <input
          ref={inputRef}
          type="text"
          className="searchbar-input"
          placeholder="Ask a research question…"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={handleKeyDown}
          autoComplete="off"
          spellCheck="false"
        />
        {query && (
          <button
            type="button"
            className="searchbar-clear"
            onClick={() => { setQuery(""); inputRef.current?.focus(); }}
            aria-label="Clear"
          >
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none"
              stroke="currentColor" strokeWidth="2.5" strokeLinecap="round">
              <line x1="18" y1="6" x2="6" y2="18" />
              <line x1="6" y1="6" x2="18" y2="18" />
            </svg>
          </button>
        )}
        <button
          type="submit"
          className={`searchbar-btn ${loading ? "searchbar-btn--loading" : ""}`}
          disabled={!query.trim() || loading}
        >
          {loading ? (
            <span className="btn-spinner" />
          ) : (
            <>Search</>
          )}
        </button>
      </form>

      <div className="searchbar-suggestions">
        <span className="suggestions-label">Try:</span>
        {suggestions.map((s) => (
          <button
            key={s}
            className="suggestion-chip"
            type="button"
            onClick={() => { setQuery(s); onSearch(s); }}
          >
            {s}
          </button>
        ))}
      </div>
    </div>
  );
}