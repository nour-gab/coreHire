import { useState } from "react";
import { useNavigate } from "react-router-dom";

import client from "../api/client";

export default function RegisterPage() {
  const navigate = useNavigate();
  const [form, setForm] = useState({
    email: "",
    username: "",
    password: "",
    role: "candidate",
  });
  const [error, setError] = useState("");

  const submit = async (event) => {
    event.preventDefault();
    setError("");
    try {
      await client.post("/auth/register/", form);
      navigate("/login");
    } catch (err) {
      setError(JSON.stringify(err?.response?.data || "Registration failed"));
    }
  };

  return (
    <div className="mx-auto flex min-h-[calc(100vh-64px)] max-w-xl items-center px-4">
      <form onSubmit={submit} className="w-full rounded-card border border-core-line bg-white p-6 shadow-card">
        <h1 className="font-display text-2xl text-core-ink">Create account</h1>

        <div className="mt-4 grid gap-3 md:grid-cols-2">
          <input
            className="rounded-lg border border-core-line px-3 py-2"
            placeholder="Email"
            value={form.email}
            onChange={(e) => setForm({ ...form, email: e.target.value })}
            required
          />
          <input
            className="rounded-lg border border-core-line px-3 py-2"
            placeholder="Username"
            value={form.username}
            onChange={(e) => setForm({ ...form, username: e.target.value })}
            required
          />
          <input
            className="rounded-lg border border-core-line px-3 py-2 md:col-span-2"
            placeholder="Password"
            type="password"
            value={form.password}
            onChange={(e) => setForm({ ...form, password: e.target.value })}
            required
          />
          <select
            className="rounded-lg border border-core-line px-3 py-2 md:col-span-2"
            value={form.role}
            onChange={(e) => setForm({ ...form, role: e.target.value })}
          >
            <option value="candidate">Candidate</option>
            <option value="company">Company</option>
            <option value="admin">Admin</option>
          </select>
        </div>

        {error ? <p className="mt-3 text-sm text-red-600">{error}</p> : null}

        <button className="mt-5 w-full rounded-lg bg-core-ink px-4 py-2 text-white" type="submit">
          Register
        </button>
      </form>
    </div>
  );
}
