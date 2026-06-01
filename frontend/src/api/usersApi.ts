import { axiosClient } from "./axiosClient";
import type { CreateUserRequest, ManagedUserResponse } from "../types/users";

export async function fetchUsers() {
  const response = await axiosClient.get<ManagedUserResponse[]>("/users");
  return response.data;
}

export async function createUser(request: CreateUserRequest) {
  const response = await axiosClient.post<ManagedUserResponse>("/users", request);
  return response.data;
}

export async function deactivateUser(userId: string) {
  const response = await axiosClient.delete<ManagedUserResponse>(`/users/${userId}`);
  return response.data;
}