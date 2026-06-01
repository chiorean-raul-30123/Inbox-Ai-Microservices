import { useEffect, useState } from "react";
import {
  Activity,
  CheckCircle2,
  Database,
  HardDrive,
  Server,
  ShieldCheck,
  XCircle,
} from "lucide-react";

import { fetchSystemOverview } from "../api/systemApi";
import { Layout } from "../components/Layout";
import { DashboardCard } from "../components/DashboardCard";
import type {
  HealthItem,
  SystemOverviewResponse,
} from "../types/system";

function StatusBadge({ status }: { status: string }) {
  return status === "UP" ? (
    <span className="flex items-center gap-2 rounded-full bg-green-50 px-3 py-1 text-xs font-semibold text-green-700">
      <CheckCircle2 size={14} />
      Operational
    </span>
  ) : (
    <span className="flex items-center gap-2 rounded-full bg-red-50 px-3 py-1 text-xs font-semibold text-red-700">
      <XCircle size={14} />
      Down
    </span>
  );
}

function HealthCard({
  item,
  icon,
}: {
  item: HealthItem;
  icon: React.ReactNode;
}) {
  return (
    <div className="rounded-2xl bg-white p-5 shadow-sm">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          {icon}
          <div>
            <h3 className="font-semibold text-slate-900">
              {item.name}
            </h3>

            {item.latencyMs !== undefined &&
              item.latencyMs !== null && (
                <p className="text-sm text-slate-500">
                  {item.latencyMs} ms
                </p>
              )}
          </div>
        </div>

        <StatusBadge status={item.status} />
      </div>
    </div>
  );
}

export function OperationsCenterPage() {
  const [overview, setOverview] =
    useState<SystemOverviewResponse | null>(null);

  const [isLoading, setIsLoading] = useState(true);

  async function loadOverview() {
    try {
      const data = await fetchSystemOverview();
      setOverview(data);
    } finally {
      setIsLoading(false);
    }
  }

  useEffect(() => {
    loadOverview();

    const interval = setInterval(
      loadOverview,
      15000,
    );

    return () => clearInterval(interval);
  }, []);

  if (isLoading || !overview) {
    return (
      <Layout>
        <p className="text-slate-600">
          Loading operations center...
        </p>
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-slate-900">
            Operations Center
          </h1>

          <p className="mt-2 text-slate-500">
            Monitor platform health, services and
            document processing activity.
          </p>
        </div>

        <div className="rounded-xl bg-white px-4 py-2 shadow-sm">
          <p className="text-xs text-slate-500">
            Last Updated
          </p>

          <p className="font-semibold text-slate-900">
            {new Date(
              overview.lastUpdated * 1000
            ).toLocaleTimeString()}
          </p>
        </div>
      </div>

      <div className="mt-10">
        <h2 className="mb-4 text-xl font-bold text-slate-900">
          Service Health
        </h2>

        <div className="grid grid-cols-1 gap-5 md:grid-cols-2 xl:grid-cols-4">
          {overview.services.map((service) => (
            <HealthCard
              key={service.name}
              item={service}
              icon={
                <Activity
                  className="text-blue-600"
                  size={22}
                />
              }
            />
          ))}
        </div>
      </div>

      <div className="mt-10">
        <h2 className="mb-4 text-xl font-bold text-slate-900">
          Infrastructure
        </h2>

        <div className="grid grid-cols-1 gap-5 md:grid-cols-2 xl:grid-cols-4">
          {overview.infrastructure.map(
            (infrastructure) => {
              let icon = (
                <Server
                  className="text-blue-600"
                  size={22}
                />
              );

              if (
                infrastructure.name.includes(
                  "PostgreSQL"
                )
              ) {
                icon = (
                  <Database
                    className="text-blue-600"
                    size={22}
                  />
                );
              }

              if (
                infrastructure.name.includes(
                  "MinIO"
                )
              ) {
                icon = (
                  <HardDrive
                    className="text-blue-600"
                    size={22}
                  />
                );
              }

              if (
                infrastructure.name.includes(
                  "ClamAV"
                )
              ) {
                icon = (
                  <ShieldCheck
                    className="text-blue-600"
                    size={22}
                  />
                );
              }

              return (
                <HealthCard
                  key={infrastructure.name}
                  item={infrastructure}
                  icon={icon}
                />
              );
            }
          )}
        </div>
      </div>

      <div className="mt-10">
        <h2 className="mb-4 text-xl font-bold text-slate-900">
          Processing Metrics
        </h2>

        <div className="grid grid-cols-1 gap-5 md:grid-cols-2 xl:grid-cols-4">
          <DashboardCard
            title="Total Documents"
            value={
              overview.summary.totalDocuments
            }
          />

          <DashboardCard
            title="Needs Review"
            value={
              overview.summary
                .needsReviewDocuments
            }
          />

          <DashboardCard
            title="Reviewed"
            value={
              overview.summary
                .reviewedDocuments
            }
          />

          <DashboardCard
            title="Average Confidence"
            value={
              overview.summary
                .averageConfidence === null
                ? "N/A"
                : `${(
                    overview.summary
                      .averageConfidence * 100
                  ).toFixed(1)}%`
            }
          />
        </div>
      </div>
    </Layout>
  );
}