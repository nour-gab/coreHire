import { useEffect, useState } from "react";

import client from "../api/client";
import Card from "../components/Card";
import ChatAssistant from "../components/ChatAssistant";
import ResumeBuilder from "../components/ResumeBuilder";

export default function CandidateDashboard() {
  const [analysis, setAnalysis] = useState(null);
  const [recommendations, setRecommendations] = useState([]);

  useEffect(() => {
    const load = async () => {
      try {
        const rec = await client.get("/ai/recommend-jobs/");
        setRecommendations(rec.data || []);
      } catch {
        setRecommendations([]);
      }
    };
    load();
  }, []);

  const runMicroSuggestions = async () => {
    const { data } = await client.post("/ai/micro-suggestions/", {
      resume_text: "I built web apps and collaborated in agile teams.",
      job_text: "Frontend internship requiring React, API integration, testing, and communication.",
    });
    setAnalysis(data);
  };

  return (
    <div className="space-y-4">
      <h1 className="font-display text-3xl text-core-ink">Candidate Dashboard</h1>
      <div className="grid gap-4 md:grid-cols-2">
        <Card title="Resume AI Assistant" subtitle="Improve your CV with micro-suggestions">
          <button
            className="rounded-lg bg-core-ink px-4 py-2 text-sm text-white transition duration-300 hover:scale-[1.02]"
            onClick={runMicroSuggestions}
          >
            Generate Suggestions
          </button>
          {analysis ? (
            <ul className="mt-3 list-disc space-y-1 pl-5 text-sm text-core-ink/80">
              {(analysis.missing_skills || []).slice(0, 5).map((skill) => (
                <li key={skill}>{skill}</li>
              ))}
            </ul>
          ) : null}
        </Card>

        <Card title="Recommended Jobs" subtitle="ATS-driven ranking based on your profile">
          <ul className="space-y-2 text-sm">
            {recommendations.slice(0, 5).map((item) => (
              <li key={item.job_id} className="rounded-lg border border-core-line px-3 py-2">
                {item.title} - Match: {item.score}%
              </li>
            ))}
            {!recommendations.length ? <li>No recommendations yet.</li> : null}
          </ul>
        </Card>
      </div>

      <ResumeBuilder />
      <ChatAssistant role="candidate" title="Candidate AI Coach" />
    </div>
  );
}
