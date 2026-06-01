import { axiosClient } from "./axiosClient";
import type { SystemOverviewResponse } from "../types/system";

export async function fetchSystemOverview() {
  const response =
    await axiosClient.get<SystemOverviewResponse>(
      "/system/overview"
    );

  return response.data;
}