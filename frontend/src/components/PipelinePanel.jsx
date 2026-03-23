import React, { useEffect, useState } from "react";
import "./PipelinePanel.css";

const PIPELINE_STEPS = [
  {
    id: "retrieve",
    label: "Retrieval & Summarization",
    description: "Fetching arXiv papers, embedding & summarizing",
    icon: "⬡",
    subSteps: [
      "Querying arXiv API",
      "Downloading PDFs",
      "Parsing & cleaning text",
      "Chunking documents",
      "Embedding with e5-large",
      "Indexing in FAISS",
      "Summarizing papers",
    ],
  },
  {
    id: "gaps",
    label: "Research Gap Analysis",
    description: "Detecting unexplored directions in the literature",
    icon: "◈",
    subSteps: [],
  },
  {
    id: "graph",
    label: "Knowledge Graph",
    description: "Mapping entities and relationships across papers",
    icon: "◎",
    subSteps: [],
  },
  {
    id: "experiments",
    label: "Experiment Ideas",
    description: "Proposing novel research directions",
    icon: "◇",
    subSteps: [],
  },
  {
    id: "compare",
    label: "Comparison Analysis",
    description: "Benchmarking methods, tradeoffs and use-cases",
    icon: "⊞",
    subSteps: [],
  },
];

// Sub-step timer delays (ms) — fake but realistic for demo
const SUB_STEP_DELAYS = [600, 1800, 3200, 5000, 7200, 9000, 11000];

export default function PipelinePanel({ steps, collapsed }) {
  const [subStepIndex, setSubStepIndex] = useState(-1);

  // Animate sub-steps while step 1 is active
  const step1Status = steps.find((s) => s.id === "retrieve")?.status;

  useEffect(() => {
    if (step1Status !== "active") {
      setSubStepIndex(-1);
      return;
    }
    setSubStepIndex(0);
    const timers = SUB_STEP_DELAYS.map((delay, i) =>
      setTimeout(() => setSubStepIndex(i), delay)
    );
    return () => timers.forEach(clearTimeout);
  }, [step1Status]);

  return (
    <div className={`pipeline-panel ${collapsed ? "pipeline-panel--collapsed" : ""}`}>
      {collapsed ? (
        <CollapsedBar steps={steps} />
      ) : (
        <ExpandedPipeline
          steps={steps}
          subStepIndex={subStepIndex}
        />
      )}
    </div>
  );
}

function CollapsedBar({ steps }) {
  const done = steps.filter((s) => s.status === "done").length;
  return (
    <div className="pipeline-collapsed-bar">
      <div className="collapsed-track">
        {steps.map((step, i) => (
          <React.Fragment key={step.id}>
            <div className={`collapsed-dot collapsed-dot--${step.status}`} title={step.label} />
            {i < steps.length - 1 && <div className="collapsed-connector" />}
          </React.Fragment>
        ))}
      </div>
      <span className="collapsed-label">
        All {done} agents complete
      </span>
    </div>
  );
}

function ExpandedPipeline({ steps, subStepIndex }) {
  return (
    <div className="pipeline-expanded">
      <div className="pipeline-heading">
        <span className="pipeline-heading-label">Running agents</span>
      </div>
      <div className="pipeline-steps">
        {PIPELINE_STEPS.map((def, i) => {
          const step = steps.find((s) => s.id === def.id) || {};
          const isActive = step.status === "active";
          const isDone   = step.status === "done";
          const isIdle   = !isActive && !isDone;

          return (
            <div key={def.id} className={`pipeline-step pipeline-step--${step.status || "idle"}`}>
              {/* Connector line */}
              {i < PIPELINE_STEPS.length - 1 && (
                <div className={`pipeline-connector ${isDone ? "pipeline-connector--done" : ""}`} />
              )}

              <div className="pipeline-step-row">
                {/* Indicator */}
                <div className={`step-indicator ${isActive ? "step-indicator--active" : ""} ${isDone ? "step-indicator--done" : ""}`}>
                  {isDone ? (
                    <svg width="12" height="12" viewBox="0 0 12 12" fill="none">
                      <polyline points="2,6 5,9 10,3" stroke="currentColor" strokeWidth="2"
                        strokeLinecap="round" strokeLinejoin="round" />
                    </svg>
                  ) : (
                    <span className="step-icon">{def.icon}</span>
                  )}
                </div>

                {/* Content */}
                <div className="step-content">
                  <div className="step-header">
                    <span className="step-label">{def.label}</span>
                    {isDone && step.stat && (
                      <span className="step-stat">{step.stat}</span>
                    )}
                    {isActive && (
                      <span className="step-processing">
                        <span className="dot-1">·</span>
                        <span className="dot-2">·</span>
                        <span className="dot-3">·</span>
                      </span>
                    )}
                  </div>
                  <div className="step-desc">{def.description}</div>

                  {/* Sub-steps for retrieval */}
                  {def.subSteps.length > 0 && (isActive || isDone) && (
                    <div className="sub-steps">
                      {def.subSteps.map((sub, si) => {
                        const subDone = isDone || si < subStepIndex;
                        const subActive = isActive && si === subStepIndex;
                        return (
                          <div
                            key={si}
                            className={`sub-step ${subDone ? "sub-step--done" : ""} ${subActive ? "sub-step--active" : ""}`}
                          >
                            <span className="sub-step-dot" />
                            {sub}
                          </div>
                        );
                      })}
                    </div>
                  )}
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}