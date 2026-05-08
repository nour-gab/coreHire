import { useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";

import client from "../api/client";
import Card from "../components/Card";
import ChatAssistant from "../components/ChatAssistant";

export default function CompanyDashboard() {
  const navigate = useNavigate();
  const [description, setDescription] = useState("");
  const [count, setCount] = useState(3);
  const [drafts, setDrafts] = useState([]);
  const [selectedIndex, setSelectedIndex] = useState(-1);
  const [saving, setSaving] = useState(false);
  const [status, setStatus] = useState("");
  const [editor, setEditor] = useState({
    title: "",
    project_overview: "",
    description: "",
    responsibilities: "",
    requirements: "",
    qualifications: "",
    skills: "",
    location: "Remote",
  });

  const selectedDraft = useMemo(
    () => (selectedIndex >= 0 ? drafts[selectedIndex] : null),
    [drafts, selectedIndex],
  );

  const generate = async () => {
    setStatus("");
    const { data } = await client.post("/ai/generate-job/", { description, count });
    const nextDrafts = data.jobs || [];
    setDrafts(nextDrafts);
    setSelectedIndex(nextDrafts.length ? 0 : -1);
    setStatus(nextDrafts.length ? `Generated ${nextDrafts.length} job drafts.` : "No drafts returned.");
    if (nextDrafts.length) {
      const first = nextDrafts[0];
      setEditor({
        title: first.title || "",
        project_overview: first.project_overview || "",
        description: first.description || description,
        responsibilities: (first.responsibilities || []).join("\n"),
        requirements: (first.requirements || []).join("\n"),
        qualifications: (first.qualifications || []).join("\n"),
        skills: (first.skills || []).join(", "),
        location: first.location || "Remote",
      });
    }
  };

  const selectDraft = (index) => {
    const draft = drafts[index];
    if (!draft) return;
    setSelectedIndex(index);
    setEditor({
      title: draft.title || "",
      project_overview: draft.project_overview || "",
      description: draft.description || description,
      responsibilities: (draft.responsibilities || []).join("\n"),
      requirements: (draft.requirements || []).join("\n"),
      qualifications: (draft.qualifications || []).join("\n"),
      skills: (draft.skills || []).join(", "),
      location: draft.location || "Remote",
    });
  };

  const updateEditor = (field, value) => {
    setEditor((current) => ({ ...current, [field]: value }));
  };

  const postJob = async () => {
    setSaving(true);
    setStatus("");
    try {
      await client.post("/jobs/", {
        title: editor.title,
        project_overview: editor.project_overview,
        description: editor.description,
        responsibilities: editor.responsibilities,
        requirements: editor.requirements,
        qualifications: editor.qualifications,
        skills: editor.skills
          .split(",")
          .map((skill) => skill.trim())
          .filter(Boolean),
        location: editor.location,
        is_active: true,
      });
      setStatus("Job posted successfully.");
      navigate("/dashboard/company/jobs");
    } catch {
      setStatus("Failed to post job. Check permissions and API connectivity.");
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="space-y-4">
      <h1 className="font-display text-3xl text-core-ink">Company Dashboard</h1>
      <div className="grid gap-5 lg:grid-cols-[280px_1fr]">
        <Card title="AI Job Generator" subtitle="Generate several drafts from one project description">
          <textarea
            className="h-36 w-full rounded-lg border border-core-line p-3 text-sm"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            placeholder="Describe the project, goals, and expected outcomes..."
          />
          <div className="mt-3 flex items-center gap-3">
            <label className="text-sm text-core-ink/70">Draft count</label>
            <input
              className="w-20 rounded-lg border border-core-line px-3 py-2 text-sm"
              type="number"
              min="1"
              max="8"
              value={count}
              onChange={(e) => setCount(Number(e.target.value))}
            />
          </div>
          <button
            className="mt-3 rounded-lg bg-core-ink px-4 py-2 text-sm text-white transition duration-300 hover:scale-[1.02]"
            onClick={generate}
          >
            Generate Drafts
          </button>
          {status ? <p className="mt-3 text-sm text-core-ink/70">{status}</p> : null}
        </Card>

        <div className="grid gap-5 lg:grid-cols-[260px_1fr]">
          <Card title="Draft Side Panel" subtitle="Click a draft to edit its full job info">
            <div className="max-h-[620px] space-y-3 overflow-y-auto pr-1">
              {drafts.length ? (
                drafts.map((draft, index) => (
                  <button
                    key={`${draft.title}-${index}`}
                    className={`w-full rounded-card border p-3 text-left transition duration-300 hover:-translate-y-0.5 hover:shadow-cardHover ${
                      selectedIndex === index
                        ? "border-core-ink bg-core-ink text-white"
                        : "border-core-line bg-white"
                    }`}
                    onClick={() => selectDraft(index)}
                  >
                    <p className="font-display text-base">{draft.title}</p>
                    <p className={`mt-1 text-xs ${selectedIndex === index ? "text-white/80" : "text-core-ink/60"}`}>
                      {(draft.skills || []).slice(0, 4).join(" · ")}
                    </p>
                  </button>
                ))
              ) : (
                <p className="text-sm text-core-ink/70">Generated drafts will appear here.</p>
              )}
            </div>
          </Card>

          <Card title="Editable Job Card" subtitle="Alter the full job info before posting">
            {selectedDraft ? (
              <div className="space-y-4">
                <div className="grid gap-3 md:grid-cols-2">
                  <div>
                    <label className="text-sm text-core-ink/70">Title</label>
                    <input
                      className="mt-1 w-full rounded-lg border border-core-line px-3 py-2 text-sm"
                      value={editor.title}
                      onChange={(e) => updateEditor("title", e.target.value)}
                    />
                  </div>
                  <div>
                    <label className="text-sm text-core-ink/70">Location</label>
                    <input
                      className="mt-1 w-full rounded-lg border border-core-line px-3 py-2 text-sm"
                      value={editor.location}
                      onChange={(e) => updateEditor("location", e.target.value)}
                    />
                  </div>
                </div>

                <div>
                  <label className="text-sm text-core-ink/70">Project Overview</label>
                  <textarea
                    className="mt-1 h-24 w-full rounded-lg border border-core-line p-3 text-sm"
                    value={editor.project_overview}
                    onChange={(e) => updateEditor("project_overview", e.target.value)}
                  />
                </div>

                <div>
                  <label className="text-sm text-core-ink/70">Description</label>
                  <textarea
                    className="mt-1 h-24 w-full rounded-lg border border-core-line p-3 text-sm"
                    value={editor.description}
                    onChange={(e) => updateEditor("description", e.target.value)}
                  />
                </div>

                <div className="grid gap-3 md:grid-cols-2">
                  <div>
                    <label className="text-sm text-core-ink/70">Responsibilities</label>
                    <textarea
                      className="mt-1 h-28 w-full rounded-lg border border-core-line p-3 text-sm"
                      value={editor.responsibilities}
                      onChange={(e) => updateEditor("responsibilities", e.target.value)}
                    />
                  </div>
                  <div>
                    <label className="text-sm text-core-ink/70">Requirements</label>
                    <textarea
                      className="mt-1 h-28 w-full rounded-lg border border-core-line p-3 text-sm"
                      value={editor.requirements}
                      onChange={(e) => updateEditor("requirements", e.target.value)}
                    />
                  </div>
                </div>

                <div>
                  <label className="text-sm text-core-ink/70">Qualifications</label>
                  <textarea
                    className="mt-1 h-24 w-full rounded-lg border border-core-line p-3 text-sm"
                    value={editor.qualifications}
                    onChange={(e) => updateEditor("qualifications", e.target.value)}
                  />
                </div>

                <div>
                  <label className="text-sm text-core-ink/70">Skills</label>
                  <input
                    className="mt-1 w-full rounded-lg border border-core-line px-3 py-2 text-sm"
                    value={editor.skills}
                    onChange={(e) => updateEditor("skills", e.target.value)}
                    placeholder="React, Python, SQL, Testing"
                  />
                </div>

                <div className="flex flex-wrap gap-3">
                  <button
                    className="rounded-lg bg-core-ink px-4 py-2 text-sm text-white transition duration-300 hover:scale-[1.02] disabled:opacity-60"
                    onClick={postJob}
                    disabled={saving}
                  >
                    {saving ? "Posting..." : "Post Job"}
                  </button>
                  <button
                    className="rounded-lg border border-core-ink px-4 py-2 text-sm text-core-ink transition duration-300 hover:bg-core-ink hover:text-white"
                    onClick={() => navigate("/dashboard/company/jobs")}
                  >
                    View My Jobs
                  </button>
                </div>
              </div>
            ) : (
              <p className="text-sm text-core-ink/70">Select a generated draft to edit its full job information here.</p>
            )}
          </Card>
        </div>
      </div>

      <ChatAssistant role="company" title="Employer AI Assistant" />
    </div>
  );
}
