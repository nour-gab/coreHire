import { useEffect, useState } from "react";

import client from "../api/client";
import Card from "../components/Card";

export default function CompanyJobsPage() {
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    let mounted = true;

    const load = async () => {
      try {
        const { data } = await client.get("/jobs/");
        if (mounted) {
          setJobs(data.results || data || []);
        }
      } catch {
        if (mounted) {
          setError("Unable to load your jobs right now.");
        }
      } finally {
        if (mounted) {
          setLoading(false);
        }
      }
    };

    load();
    return () => {
      mounted = false;
    };
  }, []);

  return (
    <div className="space-y-4">
      <div>
        <h1 className="font-display text-3xl text-core-ink">My Jobs</h1>
        <p className="mt-2 text-core-ink/70">Posted jobs appear here after you publish a generated draft.</p>
      </div>

      {loading ? <p className="text-sm text-core-ink/70">Loading your jobs...</p> : null}
      {error ? <p className="text-sm text-red-600">{error}</p> : null}

      <div className="grid gap-4 md:grid-cols-2">
        {jobs.map((job) => (
          <Card key={job.id} title={job.title} subtitle={job.location || "Posted job"}>
            <div className="space-y-3 text-sm text-core-ink/80">
              <p>
                <strong>Project Overview:</strong> {job.project_overview || job.description}
              </p>
              <p>
                <strong>Requirements:</strong> {job.requirements}
              </p>
              <p>
                <strong>Qualifications:</strong> {job.qualifications || "Not specified"}
              </p>
              <p>
                <strong>Skills:</strong> {(job.skills || []).join(", ")}
              </p>
            </div>
          </Card>
        ))}
        {!jobs.length && !loading ? <p className="text-sm text-core-ink/70">You have not posted any jobs yet.</p> : null}
      </div>
    </div>
  );
}
