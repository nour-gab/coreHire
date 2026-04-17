import { useState } from "react";

import client from "../api/client";
import Card from "../components/Card";
import ChatAssistant from "../components/ChatAssistant";

export default function CompanyDashboard() {
  const [description, setDescription] = useState("");
  const [generated, setGenerated] = useState(null);

  const generate = async () => {
    const { data } = await client.post("/ai/generate-job/", { description });
    setGenerated(data);
  };

  return (
    <div className="space-y-4">
      <h1 className="font-display text-3xl text-core-ink">Company Dashboard</h1>
      <div className="grid gap-4 md:grid-cols-2">
        <Card title="AI Job Generator" subtitle="Paste rough job description">
          <textarea
            className="h-32 w-full rounded-lg border border-core-line p-3"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            placeholder="Describe role, expectations, and outcomes..."
          />
          <button
            className="mt-3 rounded-lg bg-core-ink px-4 py-2 text-sm text-white transition duration-300 hover:scale-[1.02]"
            onClick={generate}
          >
            Generate
          </button>
        </Card>

        <Card title="Generated Output" subtitle="Edit before posting">
          {generated ? (
            <div className="space-y-2 text-sm text-core-ink/80">
              <p>
                <strong>Title:</strong> {generated.title}
              </p>
              <p>
                <strong>Skills:</strong> {(generated.skills || []).join(", ")}
              </p>
            </div>
          ) : (
            <p className="text-sm text-core-ink/70">No generated content yet.</p>
          )}
        </Card>
      </div>

      <ChatAssistant role="company" title="Employer AI Assistant" />
    </div>
  );
}
