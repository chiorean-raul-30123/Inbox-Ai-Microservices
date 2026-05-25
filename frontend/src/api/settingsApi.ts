import { axiosClient } from "./axiosClient";
import type { AiThresholdResponse, UpdateAiThresholdRequest } from "../types/settings";

export async function fetchAiThreshold() {
  const response = await axiosClient.get<AiThresholdResponse>("/settings/ai-threshold");
  return response.data;
}

export async function updateAiThreshold(request: UpdateAiThresholdRequest) {
  const response = await axiosClient.put<AiThresholdResponse>(
    "/settings/ai-threshold",
    request
  );

  return response.data;
}