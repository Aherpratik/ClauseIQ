import { useState } from "react";
import { askQuestion } from "../../services/api";

export default function AskAITab({ documentId }) {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [sources, setSources] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleAsk() {
    if (!question.trim()) return;

    try {
      setLoading(true);
      setError("");
      setAnswer("");
      setSources([]);

      const response = await askQuestion(documentId, question.trim());

      setAnswer(response.answer || "No answer returned.");
      setSources(response.sources || []);
    } catch (err) {
      console.error("Ask AI failed:", err);
      setError("Failed to get answer from document.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="space-y-4">
      <div className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
        <h3 className="text-base font-semibold text-slate-900">
          Ask a question about this document
        </h3>

        <textarea
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Ask something about this document..."
          className="mt-3 min-h-[120px] w-full rounded-md border border-slate-300 p-3 text-sm outline-none focus:border-slate-500"
        />

        <button
          onClick={handleAsk}
          disabled={loading}
          className="mt-4 rounded-lg bg-slate-900 px-4 py-2 text-sm font-medium text-white hover:bg-slate-800 disabled:opacity-60"
        >
          {loading ? "Asking..." : "Ask ClauseIQ"}
        </button>

        {error && (
          <p className="mt-3 text-sm text-red-600">
            {error}
          </p>
        )}
      </div>

      <div className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
        <h3 className="text-base font-semibold text-slate-900">Answer</h3>

        <p className="mt-3 whitespace-pre-wrap text-sm leading-7 text-slate-700">
          {answer || "No answer yet."}
        </p>

        {sources.length > 0 && (
          <div className="mt-4">
            <h4 className="text-xs font-semibold uppercase tracking-wide text-slate-500">
              Evidence
            </h4>

            <div className="mt-2 space-y-3">
            {sources.map((source, index) => (
              <div
                key={index}
                className="rounded-lg border border-slate-200 bg-slate-50 p-3 hover:bg-slate-100 transition"
              >
                <div className="flex justify-between text-xs text-slate-500 mb-1">
                  <span> Page {source.page_number}</span>
                  <span>
                     Confidence{" "}
                    {source.score
                      ? `${(source.score * 100).toFixed(1)}%`
                      : "N/A"}
                  </span>
                </div>

                <p className="text-sm text-slate-700 line-clamp-3">
                  {source.text}
                </p>
              </div>
            ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}