import { useState } from "react";

import client from "../api/client";

export default function ChatAssistant({ role = "candidate", title = "AI Assistant" }) {
  const [message, setMessage] = useState("");
  const [reply, setReply] = useState("");
  const [loading, setLoading] = useState(false);

  const ask = async () => {
    if (!message.trim()) return;
    setLoading(true);
    try {
      const { data } = await client.post("/ai/chat/", { role, message });
      setReply(data.reply || "No response.");
    } catch {
      setReply("Assistant unavailable. Check API auth and connectivity.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="rounded-card border border-core-line bg-white p-4 shadow-card">
      <h3 className="font-display text-lg text-core-ink">{title}</h3>
      <textarea
        className="mt-3 h-24 w-full rounded-lg border border-core-line p-3 text-sm"
        placeholder="Ask anything..."
        value={message}
        onChange={(e) => setMessage(e.target.value)}
      />
      <button
        className="mt-3 rounded-lg bg-core-ink px-3 py-2 text-sm text-white transition duration-300 hover:scale-[1.02]"
        onClick={ask}
        disabled={loading}
      >
        {loading ? "Thinking..." : "Ask Assistant"}
      </button>
      {reply ? <p className="mt-3 text-sm text-core-ink/80">{reply}</p> : null}
    </div>
  );
}
