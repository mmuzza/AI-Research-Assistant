import React, { useState } from "react";
import "./PaperCard.css";

export default function PaperCard({ paper, index }) {
  const [expanded, setExpanded] = useState(false);

  const summary = paper.summary || paper.chunk_text || "";
  const preview = summary.slice(0, 260);
  const hasMore = summary.length > 260;

  const authors = Array.isArray(paper.authors)
    ? paper.authors
    : typeof paper.authors === "string"
    ? paper.authors.split(",").map((a) => a.trim())
    : [];

  const firstAuthor = authors[0] || "";
  const extraAuthors = authors.length > 3 ? `+${authors.length - 3} more` : null;
  const displayAuthors = authors.slice(0, 3);

  return (
    <article
      className="paper-card"
      style={{ animationDelay: `${index * 60}ms` }}
    >
      <div className="paper-card-inner">
        {/* Index badge */}
        <div className="paper-index">{String(index + 1).padStart(2, "0")}</div>

        <div className="paper-body">
          {/* Title */}
          <h2 className="paper-title">
            {paper.title || "Untitled Paper"}
          </h2>

          {/* Meta row */}
          <div className="paper-meta">
            {displayAuthors.length > 0 && (
              <div className="paper-authors">
                <span>{displayAuthors.join(", ")}</span>
                {extraAuthors && <span className="extra-authors">{extraAuthors}</span>}
              </div>
            )}

          </div>

          {/* Summary */}
          {summary && (
            <div className="paper-summary">
              <p>
                {expanded ? summary : preview}
                {!expanded && hasMore && (
                  <span className="ellipsis">…</span>
                )}
              </p>
              {hasMore && (
                <button
                  className="expand-btn"
                  onClick={() => setExpanded(!expanded)}
                >
                  {expanded ? "Show less ↑" : "Read more ↓"}
                </button>
              )}
            </div>
          )}

          {/* Footer */}
          <div className="paper-footer">
            {paper.pdf_url && (
              <a
                href={paper.pdf_url}
                target="_blank"
                rel="noopener noreferrer"
                className="pdf-link"
              >
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none"
                  stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
                  <polyline points="14 2 14 8 20 8" />
                </svg>
                View PDF
              </a>
            )}
            {paper.paper_id && (
              <span className="paper-id">
                arXiv:{paper.paper_id}
              </span>
            )}
          </div>
        </div>
      </div>
    </article>
  );
}