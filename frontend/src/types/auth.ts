export type LoginRequest = {
  email: string;
  password: string;
};

export type TokenResponse = {
  access_token: string;
  token_type: string;
};

export type RoleResponse = {
  id: number;
  name: string;
  description: string | null;
};

export type UserResponse = {
  id: string;
  full_name: string;
  email: string;
  is_active: boolean;
  role: RoleResponse;
  created_at: string;
  updated_at: string;
};