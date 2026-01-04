"use client"; // Tells Next.js the component runs in the browser (for form state and click handlers)
import { useRouter } from "next/navigation"; // Import useRouter for client-side navigation after successful authentication
import React, { useState } from "react"; // Import useState for managing component states

export default function LoginClient() {
  const router = useRouter(); // Create a router instance to navigate after successful authentication

  const [email, setEmail] = useState(""); // Store the email input value in React state, initializing it as a empty string
  const [password, setPassword] = useState(""); // Store the password input value in React state, initializing it as a empty string
  const [isSubmitting, setIsSubmitting] = useState(false); // Track submission state to enable or disable the button to prevent multiple requests
  const [error, setError] = useState<string | null>(null); // Store error message to display to client if login fails

  async function handlePasswordLogin(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault(); // Prevent the browser from doing normal HTML form submission

    setError(null); // Clear prior errors before attempting again.
    setIsSubmitting(true); // Turn on loading state for button

    // Call your existing login endpoint
    const loginRes = await fetch("/api/auth/login", {
      method: "POST",
      headers: { "content-type": "application/json" },
      credentials: "include", // Include credentials int he headers so the browser will store the session cookie
      body: JSON.stringify({ email, password }),
    });

    // If login response not ok, show the returned error by updating the error state
    if (!loginRes.ok) {
      const data = await loginRes.json().catch(() => ({}));
      setError(data?.error ?? "Login Failed");
      setIsSubmitting(false);
      return;
    }

    // Login success brings you to transactions page
    router.push("/transactions");
    router.refresh(); // Refresh so server components are able to see the new cookie
    setIsSubmitting(false);
  }

  // Handles Google Oauth by redirecting to /api/auth/google/start endpoint
  async function handleGoogleLogin() {
    /*
     * Triggers this flow:
     * 1. Get /api/auth/google/start
     * 2. Redirect to Google consent screen
     * 3. Google redirects back to /api/auth/google/callback
     * 4. Call back sets SESSION_COOKIE_NAME and redirects to APP_URL
     */
    window.localStorage.href = "/api/auth/google/start";
  }

  return (
    <main className="min-h-screen bg-zinc-950 text-zinc-100 flex items-center justify-center px-4">
      <div className="w-full max-w-md rounded-2xl border border-zinc-800 bg-zinc-900/40 p-6 shadow-lg">
        <h1 className="text-2xl font-semibold tracking-tight">Login</h1>
        <p className="mt-1 text-sm text-zinc-400">
          Sign in to add expenses and view your ledger.
        </p>

        {/* Google OAuth button */}
        {/* <button
          type="button" // Not a form submit.
          onClick={handleGoogleLogin} // Starts your OAuth flow.
          className="mt-6 w-full rounded-xl border border-zinc-800 bg-zinc-950/40 px-4 py-2 text-sm font-semibold text-zinc-100 hover:border-zinc-600"
        >
          Continue with Google
        </button> */}
        <a
          href="/api/auth/google/start"
          className="mt-6 block w-full rounded-xl border border-zinc-800 bg-zinc-950/40 px-4 py-2 text-center text-sm font-semibold text-zinc-100 hover:border-zinc-600"
        >
          Continue with Google
        </a>
        {/* Divider */}
        <div className="my-6 flex items-center gap-3">
          <div className="h-px flex-1 bg-zinc-800" />
          <span className="text-xs text-zinc-500">or</span>
          <div className="h-px flex-1 bg-zinc-800" />
        </div>

        {/* Password login form */}
        <form onSubmit={handlePasswordLogin} className="space-y-4">
          {error && (
            <div className="rounded-xl border border-red-900/60 bg-red-950/40 px-4 py-3 text-sm text-red-200">
              {error}
            </div>
          )}

          <div className="space-y-2">
            <label className="text-sm font-medium text-zinc-200">Email</label>
            <input
              value={email} // Bind state -> input
              onChange={(e) => setEmail(e.target.value)} // Update state on typing
              type="email"
              required
              className="w-full rounded-xl border border-zinc-800 bg-zinc-950/40 px-3 py-2 text-zinc-100 placeholder:text-zinc-600 outline-none focus:border-zinc-600"
              placeholder="you@example.com"
            />
          </div>

          <div className="space-y-2">
            <label className="text-sm font-medium text-zinc-200">
              Password
            </label>
            <input
              value={password} // Bind state -> input
              onChange={(e) => setPassword(e.target.value)} // Update state on typing
              type="password"
              required
              className="w-full rounded-xl border border-zinc-800 bg-zinc-950/40 px-3 py-2 text-zinc-100 placeholder:text-zinc-600 outline-none focus:border-zinc-600"
              placeholder="••••••••"
            />
          </div>

          <button
            type="submit"
            disabled={isSubmitting} // Prevent double submit.
            className="w-full rounded-xl bg-zinc-100 px-4 py-2 text-sm font-semibold text-zinc-950 transition hover:bg-white disabled:cursor-not-allowed disabled:opacity-70"
          >
            {isSubmitting ? "Logging in..." : "Login"}
          </button>
        </form>
      </div>
    </main>
  );
}
