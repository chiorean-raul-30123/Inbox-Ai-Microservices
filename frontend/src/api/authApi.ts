import { axiosClient } from "./axiosClient";
import type { LoginRequest, TokenResponse, UserResponse } from "../types/auth";

export async function login(request: LoginRequest) {
    const response = await axiosClient.post<TokenResponse>("/auth/login",request);
    return response.data;
}

export async function getMe(){
    const response = await axiosClient.get<UserResponse>("/auth/me");
    return response.data;
}

export type ChangePasswordRequest = {
  current_password: string;
  new_password: string;
};

export async function changePassword(request: ChangePasswordRequest) {
  const response = await axiosClient.post<UserResponse>(
    "/users/me/change-password",
    request,
  );

  return response.data;
}