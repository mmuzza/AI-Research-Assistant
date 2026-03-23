// import axios from "axios";
// export const searchPapers = async (query) => {
//   try {
//     const response = await axios.post("http://127.0.0.1:8000/query", { query });
//     return response.data;
//   } catch (err) {
//     console.error("API request failed:", err);
//     return { retrieved_papers: [], paper_summaries: [], summary: "" };
//   }
// };


import axios from "axios";
 
const BASE = "http://127.0.0.1:8000";
 
const post = async (path, body) => {
  const res = await axios.post(`${BASE}${path}`, body);
  return res.data;
};
 
export const retrievePapers   = (query)                          => post("/query/retrieve",    { query });
export const fetchGaps        = (paper_summaries)                => post("/query/gaps",        { paper_summaries });
export const fetchGraph       = (paper_summaries)                => post("/query/graph",       { paper_summaries });
export const fetchExperiments = (paper_summaries, research_gaps) => post("/query/experiments", { paper_summaries, research_gaps });
export const fetchComparison  = (paper_summaries)                => post("/query/compare",     { paper_summaries });