import { useState } from "react";
import { useNavigate } from "react-router-dom";

import client from "../api/client";

export default function LoginPage() {
  const navigate = useNavigate();
  const [form, setForm] = useState({ email: "", password: "" });
  const [error, setError] = useState("");

  const submit = async (event) => {
    event.preventDefault();
    setError("");

    try {
      const { data } = await client.post("/auth/login/", form);
      localStorage.setItem("accessToken", data.access);
      localStorage.setItem("refreshToken", data.refresh);

      const me = await client.get("/auth/me/");
      const role = me.data?.user?.role || "candidate";

      if (role === "company") navigate("/dashboard/company");
      else if (role === "admin") navigate("/dashboard/admin");
      else navigate("/dashboard/candidate");
    } catch (err) {
      setError(err?.response?.data?.detail || "Login failed.");
    }
  };

  return (
    <div className="mx-auto flex min-h-[calc(100vh-64px)] max-w-md items-center px-4">
      <form onSubmit={submit} className="w-full rounded-card border border-core-line bg-white p-6 shadow-card">
        <h1 className="font-display text-2xl text-core-ink">Welcome back</h1>
        <p className="mt-1 text-sm text-core-ink/70">Sign in to access your CoreHire dashboard.</p>

        <label className="mt-5 block text-sm text-core-ink">Email</label>
        <input
          className="mt-1 w-full rounded-lg border border-core-line px-3 py-2"
          type="email"
          value={form.email}
          onChange={(e) => setForm({ ...form, email: e.target.value })}
          required
        />

        <label className="mt-3 block text-sm text-core-ink">Password</label>
        <input
          className="mt-1 w-full rounded-lg border border-core-line px-3 py-2"
          type="password"
          value={form.password}
          onChange={(e) => setForm({ ...form, password: e.target.value })}
          required
        />

        {error ? <p className="mt-3 text-sm text-red-600">{error}</p> : null}

        <button
          className="mt-5 w-full rounded-lg bg-core-ink px-4 py-2 text-white transition duration-300 hover:scale-[1.01] hover:opacity-90"
          type="submit"
        >
          Login
        </button>
      </form>
    </div>
  );
}
