import { useEffect, useState } from "react";

import { fetchAiThreshold, updateAiThreshold } from "../api/settingsApi";
import { Layout } from "../components/Layout";

export function SettingsPage() {
  const [threshold, setThreshold] = useState("0.85");
  const [isLoading, setIsLoading] = useState(true);
  const [isSaving, setIsSaving] = useState(false);
  const [message, setMessage] = useState("");
  const [errorMessage, setErrorMessage] = useState("");

  async function loadThreshold() {
    try {
      const data = await fetchAiThreshold();
      setThreshold(String(data.threshold));
    } catch {
      setErrorMessage("Could not load AI threshold.");
    } finally {
      setIsLoading(false);
    }
  }

  async function handleSave() {
    setMessage("");
    setErrorMessage("");

    const parsedThreshold = Number(threshold);

    if (Number.isNaN(parsedThreshold) || parsedThreshold < 0 || parsedThreshold > 1) {
      setErrorMessage("Threshold must be a number between 0 and 1.");
      return;
    }

    try {
      setIsSaving(true);
      const data = await updateAiThreshold({ threshold: parsedThreshold });
      setThreshold(String(data.threshold));
      setMessage("AI threshold updated successfully.");
    } catch {
      setErrorMessage("Could not update AI threshold.");
    } finally {
      setIsSaving(false);
    }
  }

  useEffect(() => {
    loadThreshold();
  }, []);

  return (
    <Layout>
      <div>
        <h1 className="text-3xl font-bold text-slate-900">Settings</h1>
        <p className="mt-2 text-slate-500">
          Configure system-level AI routing behavior.
        </p>
      </div>

      <div className="mt-8 max-w-xl rounded-2xl bg-white p-6 shadow-sm">
        <label className="text-sm font-medium text-slate-700">
          AI Confidence Threshold
        </label>

        <input
          value={threshold}
          onChange={(event) => setThreshold(event.target.value)}
          disabled={isLoading}
          className="mt-2 w-full rounded-lg border border-slate-300 px-3 py-2 outline-none focus:border-slate-900"
          type="number"
          min="0"
          max="1"
          step="0.01"
        />

        <p className="mt-2 text-sm text-slate-500">
          Documents below this confidence are sent to Needs Review.
        </p>

        {message && (
          <div className="mt-4 rounded-lg bg-green-50 p-3 text-sm text-green-700">
            {message}
          </div>
        )}

        {errorMessage && (
          <div className="mt-4 rounded-lg bg-red-50 p-3 text-sm text-red-700">
            {errorMessage}
          </div>
        )}

        <button
          onClick={handleSave}
          disabled={isSaving || isLoading}
          className="mt-6 rounded-lg bg-slate-900 px-4 py-2 font-medium text-white hover:bg-slate-800 disabled:opacity-50"
        >
          {isSaving ? "Saving..." : "Save Settings"}
        </button>
      </div>
    </Layout>
  );
}