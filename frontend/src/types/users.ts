import type { UserResponse } from "./auth";

export type CreateUserRequest = {
  full_name: string;
  email: string;
  password: string;
  role_id: number;
};

export type ManagedUserResponse = UserResponse;

export type RoleOption = {
  id: number;
  name: "ADMIN" | "HR" | "FINANCE" | "LEGAL";
  label: string;
};

export const roleOptions: RoleOption[] = [
  { id: 1, name: "ADMIN", label: "Admin" },
  { id: 2, name: "HR", label: "HR" },
  { id: 3, name: "FINANCE", label: "Finance" },
  { id: 4, name: "LEGAL", label: "Legal" },
];