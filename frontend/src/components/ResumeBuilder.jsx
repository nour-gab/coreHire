import { useMemo, useState } from "react";

const initialState = {
  personal: "Name, Email, Phone, LinkedIn",
  education: "Degree, University, Year",
  experience: "Role, Company, impact bullets",
  projects: "Project name, stack, measurable outcome",
  skills: "Python, React, SQL, Git",
};

export default function ResumeBuilder() {
  const [sections, setSections] = useState(initialState);

  const preview = useMemo(
    () => [
      { key: "personal", label: "Personal Info" },
      { key: "education", label: "Education" },
      { key: "experience", label: "Experience" },
      { key: "projects", label: "Projects" },
      { key: "skills", label: "Skills" },
    ],
    [],
  );

  return (
    <div className="grid gap-4 md:grid-cols-2">
      <div className="rounded-card border border-core-line bg-white p-4 shadow-card">
        <h3 className="font-display text-lg text-core-ink">Resume Builder</h3>
        <div className="mt-3 space-y-3">
          {preview.map((item) => (
            <div key={item.key}>
              <label className="text-sm text-core-ink/75">{item.label}</label>
              <textarea
                className="mt-1 h-20 w-full rounded-lg border border-core-line p-2 text-sm"
                value={sections[item.key]}
                onChange={(e) => setSections((old) => ({ ...old, [item.key]: e.target.value }))}
              />
            </div>
          ))}
        </div>
        <button
          className="mt-3 rounded-lg bg-core-moss px-3 py-2 text-sm font-semibold text-core-ink transition duration-300 hover:scale-[1.02]"
          onClick={() => window.print()}
        >
          Export to PDF
        </button>
      </div>

      <div className="rounded-card border border-core-line bg-white p-4 shadow-card">
        <h3 className="font-display text-lg text-core-ink">Live Preview</h3>
        <div className="mt-3 space-y-3 text-sm text-core-ink/85">
          {preview.map((item) => (
            <section key={item.key}>
              <h4 className="font-display text-base text-core-ink">{item.label}</h4>
              <p className="whitespace-pre-wrap">{sections[item.key]}</p>
            </section>
          ))}
        </div>
      </div>
    </div>
  );
}
