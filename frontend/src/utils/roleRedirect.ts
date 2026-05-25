import type { UserResponse } from "../types/auth";

export function getHomePathForUser(user: UserResponse) {
  const roleName = user.role.name;

  if (roleName === "ADMIN") {
    return "/";
  }

  if (roleName === "HR") {
    return "/inbox/hr";
  }

  if (roleName === "FINANCE") {
    return "/inbox/finance";
  }

  if (roleName === "LEGAL") {
    return "/inbox/legal";
  }

  return "/login";
}