import { Link } from "react-router-dom";

export default function Navbar() {
  return (
    <header className="sticky top-0 z-30 border-b border-core-line bg-core-cloud/90 backdrop-blur">
      <nav className="mx-auto flex max-w-6xl items-center justify-between px-4 py-3 md:px-6">
        <Link to="/" className="font-display text-xl text-core-ink">
          CoreHire
        </Link>
        <div className="flex items-center gap-2 text-sm md:gap-4">
          <Link className="rounded-lg px-3 py-1.5 text-core-ink transition hover:bg-core-teal/20" to="/jobs">
            Jobs
          </Link>
          <Link className="rounded-lg px-3 py-1.5 text-core-ink transition hover:bg-core-teal/20" to="/login">
            Login
          </Link>
          <Link
            className="rounded-lg bg-core-ink px-3 py-1.5 text-white transition hover:scale-[1.02] hover:opacity-90"
            to="/register"
          >
            Get Started
          </Link>
        </div>
      </nav>
    </header>
  );
}
