import { motion } from "framer-motion";
import { Link } from "react-router-dom";

import AnimatedHeroLines from "../components/AnimatedHeroLines";
import Card from "../components/Card";

const features = [
  "ATS scoring with KeyBERT keyword extraction",
  "AI resume micro-suggestions and project recommendations",
  "Company-side AI job generation and JD optimization",
  "Role-based dashboards for candidates, companies, and admins",
];

export default function LandingPage() {
  return (
    <div className="relative min-h-[calc(100vh-64px)] overflow-hidden bg-core-cloud">
      <AnimatedHeroLines />
      <section className="relative mx-auto max-w-6xl px-4 pb-10 pt-14 md:px-6 md:pt-20">
        <motion.div initial={{ opacity: 0, y: 24 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.7 }}>
          <p className="font-body text-xs uppercase tracking-[0.22em] text-core-ink/65">AI-Powered Hiring Intelligence</p>
          <h1 className="mt-3 max-w-3xl font-display text-4xl leading-tight text-core-ink md:text-6xl">
            Match candidates and companies with sharper, data-driven decisions.
          </h1>
          <p className="mt-5 max-w-2xl text-base text-core-ink/75 md:text-lg">
            CoreHire combines resume analysis, ATS scoring, and role-aware dashboards into one focused recruitment workflow.
          </p>
          <div className="mt-8 flex flex-wrap gap-3">
            <Link
              to="/register"
              className="rounded-lg bg-core-ink px-5 py-3 text-sm font-semibold text-white transition duration-300 hover:scale-[1.03] hover:opacity-90"
            >
              Create Account
            </Link>
            <Link
              to="/jobs"
              className="rounded-lg border border-core-ink px-5 py-3 text-sm font-semibold text-core-ink transition duration-300 hover:scale-[1.03] hover:bg-core-ink hover:text-white"
            >
              Explore Jobs
            </Link>
          </div>
        </motion.div>

        <div className="mt-12 grid grid-cols-1 gap-4 md:grid-cols-2">
          {features.map((feature, idx) => (
            <motion.div
              key={feature}
              initial={{ opacity: 0, y: 18 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: idx * 0.12, duration: 0.5 }}
            >
              <Card title={`Core Feature ${idx + 1}`} subtitle={feature}>
                <p className="text-sm text-core-ink/75">
                  Purpose-built for internship and early-career recruitment with practical AI insights, not black-box noise.
                </p>
              </Card>
            </motion.div>
          ))}
        </div>
      </section>
    </div>
  );
}
