
import React, { useRef, useCallback } from "react";
import ForceGraph2D from "react-force-graph-2d";


const NODE_COLORS = {
  concept: "#f0a500",
  model:   "#60a5fa",
  method:  "#4ade80",
  dataset: "#c084fc",
  default: "#8a92a6",
};

const LINK_COLOR = "rgba(255,255,255,0.12)";
const HIGHLIGHT_LINK = "rgba(240,165,0,0.5)";

export default function KnowledgeGraph({ graph }) {
  const fgRef = useRef();

  const graphData = {
    nodes: (graph.nodes || []).map((n) => ({
      id:    n.id,
      type:  n.type || "default",
      label: n.id,
      color: NODE_COLORS[n.type] || NODE_COLORS.default,
    })),
    links: (graph.edges || []).map((e) => ({
      source:   e.source,
      target:   e.target,
      relation: e.relation,
    })),
  };

  const handleNodeClick = useCallback((node) => {
    if (fgRef.current) {
      fgRef.current.centerAt(node.x, node.y, 600);
      fgRef.current.zoom(3, 600);
    }
  }, []);

  const drawNode = useCallback((node, ctx, globalScale) => {
    const r     = 6;
    const label = node.label;
    const fs    = Math.max(10 / globalScale, 3);


    ctx.shadowColor  = node.color;
    ctx.shadowBlur   = 8;


    ctx.beginPath();
    ctx.arc(node.x, node.y, r, 0, 2 * Math.PI);
    ctx.fillStyle = node.color;
    ctx.fill();


    ctx.beginPath();
    ctx.arc(node.x, node.y, r * 0.35, 0, 2 * Math.PI);
    ctx.fillStyle = "rgba(0,0,0,0.6)";
    ctx.fill();

    ctx.shadowBlur = 0;


    ctx.font         = `${fs}px 'Source Sans 3', sans-serif`;
    ctx.textAlign    = "center";
    ctx.textBaseline = "middle";
    ctx.fillStyle    = "rgba(234,237,245,0.85)";
    ctx.fillText(label, node.x, node.y + r + fs * 0.8);
  }, []);

  const linkColor = useCallback(() => LINK_COLOR, []);

  const linkLabel = useCallback((link) => link.relation || "", []);

  const drawLink = useCallback((link, ctx) => {
    const start = link.source;
    const end   = link.target;
    if (!start || !end || typeof start !== "object") return;

    ctx.strokeStyle = LINK_COLOR;
    ctx.lineWidth   = 1;
    ctx.beginPath();
    ctx.moveTo(start.x, start.y);
    ctx.lineTo(end.x, end.y);
    ctx.stroke();


    if (link.relation) {
      const mx = (start.x + end.x) / 2;
      const my = (start.y + end.y) / 2;
      ctx.font      = "9px 'Source Sans 3', sans-serif";
      ctx.fillStyle = "rgba(240,165,0,0.6)";
      ctx.textAlign = "center";
      ctx.fillText(link.relation, mx, my);
    }
  }, []);

  return (
    <ForceGraph2D
      ref={fgRef}
      graphData={graphData}
      backgroundColor="#111827"
      nodeCanvasObject={drawNode}
      nodeCanvasObjectMode={() => "replace"}
      linkCanvasObject={drawLink}
      linkCanvasObjectMode={() => "replace"}
      linkColor={linkColor}
      linkLabel={linkLabel}
      onNodeClick={handleNodeClick}
      nodeLabel={(n) => `${n.id} (${n.type})`}
      cooldownTicks={120}
      linkDirectionalArrowLength={5}
      linkDirectionalArrowRelPos={1}
      linkDirectionalArrowColor={() => "rgba(240,165,0,0.5)"}
      d3AlphaDecay={0.02}
      d3VelocityDecay={0.3}
      width={undefined}
      height={460}
    />
  );
}