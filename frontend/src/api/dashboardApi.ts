import { axiosClient } from "./axiosClient";
import type { DashboardSummaryResponse } from "../types/dashboard";

export async function fetchDashboardSummary(){
    const response = await axiosClient.get<DashboardSummaryResponse>("/dashboard/summary");
    return response.data;
}