import type { DashboardSummaryResponse } from "./dashboard";

export type HealthItem = {
  name: string;
  status: "UP" | "DOWN";
  latencyMs?: number | null;
};

export type SystemOverviewResponse = {
  services: HealthItem[];
  infrastructure: HealthItem[];
  summary: DashboardSummaryResponse;
  lastUpdated: number;
};