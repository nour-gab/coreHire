import { useEffect, useState } from "react";

import client from "../api/client";
import Card from "../components/Card";

export default function JobsPage() {
  const [jobs, setJobs] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    const load = async () => {
      try {
        const { data } = await client.get("/jobs/");
        setJobs(data.results || data);
      } catch {
        setError("Unable to load jobs. Log in or verify API connection.");
      }
    };
    load();
  }, []);

  return (
    <div className="mx-auto max-w-6xl px-4 py-8 md:px-6">
      <h1 className="font-display text-3xl text-core-ink">Open Roles</h1>
      <p className="mt-2 text-core-ink/70">Browse opportunities matched for internships and entry-level careers.</p>

      {error ? <p className="mt-4 text-sm text-red-600">{error}</p> : null}

      <div className="mt-6 grid gap-4 md:grid-cols-2">
        {jobs.map((job) => (
          <Card key={job.id} title={job.title} subtitle={job.company_email || "Company"}>
            <p className="line-clamp-3 text-sm text-core-ink/75">{job.description}</p>
            <button
              className="mt-4 rounded-lg bg-core-teal px-3 py-2 text-sm font-semibold text-core-ink transition duration-300 hover:scale-[1.02]"
              onClick={async () => {
                try {
                  await client.post("/applications/", { job: job.id });
                  alert("Application sent.");
                } catch {
                  alert("Please login as candidate to apply.");
                }
              }}
            >
              Apply
            </button>
          </Card>
        ))}
      </div>
    </div>
  );
}
