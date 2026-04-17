import Card from "../components/Card";

const stats = [
  { title: "Users", value: "1,240" },
  { title: "Applications", value: "8,412" },
  { title: "Top Skills", value: "React, Python, SQL" },
];

export default function AdminDashboard() {
  return (
    <div className="space-y-4">
      <h1 className="font-display text-3xl text-core-ink">Admin Dashboard</h1>
      <div className="grid gap-4 md:grid-cols-3">
        {stats.map((stat) => (
          <Card key={stat.title} title={stat.title} subtitle="Platform analytics snapshot">
            <p className="font-display text-2xl text-core-ink">{stat.value}</p>
          </Card>
        ))}
      </div>
      <Card title="Moderation" subtitle="Review listings and user reports">
        <p className="text-sm text-core-ink/80">Use admin APIs to manage users, jobs, and flagged content.</p>
      </Card>
    </div>
  );
}
