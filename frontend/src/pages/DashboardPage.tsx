import { useEffect, useState } from "react";

import { fetchDashboardSummary } from "../api/dashboardApi";
import { DashboardCard } from "../components/DashboardCard";
import { Layout } from "../components/Layout";
import type { DashboardSummaryResponse } from "../types/dashboard";

export function DashboardPage() {
  const [summary, setSummary] = useState<DashboardSummaryResponse | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [errorMessage, setErrorMessage] = useState("");

  async function loadDashboardSummary() {
    try {
      const data = await fetchDashboardSummary();
      setSummary(data);
    } catch {
      setErrorMessage("Could not load dashboard summary.");
    } finally {
      setIsLoading(false);
    }
  }

  useEffect(() => {
    loadDashboardSummary();
  }, []);

  if (isLoading) {
    return (
      <Layout>
        <p className="text-slate-600">Loading dashboard...</p>
      </Layout>
    );
  }

  if (errorMessage || !summary) {
    return (
      <Layout>
        <div className="rounded-xl bg-red-50 p-4 text-red-700">{errorMessage}</div>
      </Layout>
    );
  }

  return (
    <Layout>
      <div>
        <h1 className="text-3xl font-bold text-slate-900">Dashboard</h1>
        <p className="mt-2 text-slate-500">Overview of document routing activity.</p>
      </div>

      <div className="mt-8 grid grid-cols-1 gap-5 md:grid-cols-2 xl:grid-cols-4">
        <DashboardCard title="Total Documents" value={summary.totalDocuments} />
        <DashboardCard title="Unsorted" value={summary.unsortedDocuments} />
        <DashboardCard title="Routed" value={summary.routedDocuments} />
        <DashboardCard title="Needs Review" value={summary.needsReviewDocuments} />
        <DashboardCard title="Reviewed" value={summary.reviewedDocuments} />
        <DashboardCard title="HR Documents" value={summary.hrDocuments} />
        <DashboardCard title="Finance Documents" value={summary.financeDocuments} />
        <DashboardCard title="Legal Documents" value={summary.legalDocuments} />
      </div>

      <div className="mt-6 rounded-2xl bg-white p-6 shadow-sm">
        <p className="text-sm font-medium text-slate-500">Average AI Confidence</p>
        <p className="mt-3 text-3xl font-bold text-slate-900">
          {summary.averageConfidence === null
            ? "N/A"
            : `${(summary.averageConfidence * 100).toFixed(1)}%`}
        </p>
      </div>
    </Layout>
  );
}