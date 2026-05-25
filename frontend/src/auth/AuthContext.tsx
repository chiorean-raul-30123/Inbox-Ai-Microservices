import { createContext, useContext, useEffect, useState } from "react";
import type { ReactNode } from "react";

import { getMe, login } from "../api/authApi";
import type { LoginRequest, UserResponse } from "../types/auth";
import { removeToken, saveToken, getToken } from "../utils/tokenStorage";

type AuthContextType = {
  user: UserResponse | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  loginUser: (request: LoginRequest) => Promise<UserResponse>;
  logoutUser: () => void;
};

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<UserResponse | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  async function loadCurrentUser() {
    const token = getToken();

    if (!token) {
      setIsLoading(false);
      return;
    }

    try {
      const currentUser = await getMe();
      setUser(currentUser);
    } catch {
      removeToken();
      setUser(null);
    } finally {
      setIsLoading(false);
    }
  }

  async function loginUser(request: LoginRequest) {
    const tokenResponse = await login(request);
    saveToken(tokenResponse.access_token);

    const currentUser = await getMe();
    setUser(currentUser);

    return currentUser;
  }

  function logoutUser() {
    removeToken();
    setUser(null);
  }

  useEffect(() => {
    loadCurrentUser();
  }, []);

  return (
    <AuthContext.Provider
      value={{
        user,
        isLoading,
        isAuthenticated: user !== null,
        loginUser,
        logoutUser,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);

  if (!context) {
    throw new Error("useAuth must be used inside AuthProvider.");
  }

  return context;
}