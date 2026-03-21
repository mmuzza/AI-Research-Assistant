import axios from "axios";
export const searchPapers = async (query) => {
  try {
    const response = await axios.post("http://127.0.0.1:8000/query", { query });
    return response.data;
  } catch (err) {
    console.error("API request failed:", err);
    return { retrieved_papers: [], paper_summaries: [], summary: "" };
  }
};