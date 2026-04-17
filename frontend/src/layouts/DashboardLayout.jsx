import { Link, Outlet } from "react-router-dom";

const linksByRole = {
  candidate: [
    { to: "/dashboard/candidate", label: "Overview" },
    { to: "/jobs", label: "Browse Jobs" },
  ],
  company: [
    { to: "/dashboard/company", label: "Overview" },
    { to: "/dashboard/company/jobs", label: "My Jobs" },
  ],
  admin: [
    { to: "/dashboard/admin", label: "Overview" },
    { to: "/jobs", label: "All Jobs" },
  ],
};

export default function DashboardLayout({ role = "candidate" }) {
  const links = linksByRole[role] || linksByRole.candidate;

  return (
    <div className="min-h-screen bg-core-cloud">
      <div className="mx-auto grid max-w-6xl grid-cols-1 gap-5 px-4 py-6 md:grid-cols-[220px_1fr] md:px-6">
        <aside className="rounded-card border border-core-line bg-white p-4 shadow-card">
          <h2 className="font-display text-lg text-core-ink">{role.toUpperCase()}</h2>
          <nav className="mt-4 flex flex-col gap-2 text-sm">
            {links.map((item) => (
              <Link
                key={item.to}
                to={item.to}
                className="rounded-lg px-3 py-2 text-core-ink transition hover:bg-core-teal/20"
              >
                {item.label}
              </Link>
            ))}
          </nav>
        </aside>
        <main>
          <Outlet />
        </main>
      </div>
    </div>
  );
}
