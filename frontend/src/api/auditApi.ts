import { axiosClient } from "./axiosClient";
import type { AuditResponse } from "../types/audit";

export async function fetchAuditLogs() {
  const response =
    await axiosClient.get<AuditResponse[]>(
      "/audit"
    );

  return response.data;
}