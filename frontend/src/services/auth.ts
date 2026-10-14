import { request } from "./api";

export interface User {
  id: number;
  name: string;
  email: string;
  role: string;
  is_active: boolean;
  created_at: string | null;
}

interface TokenResponse {
  access_token: string;
  token_type: string;
}

export function registerUser(data: {
  name: string;
  email: string;
  password: string;
}): Promise<User> {
  return request<User>("/api/auth/register", {
    method: "POST",
    body: JSON.stringify(data),
  });
}

export function loginUser(data: {
  email: string;
  password: string;
}): Promise<TokenResponse> {
  return request<TokenResponse>("/api/auth/login", {
    method: "POST",
    body: JSON.stringify(data),
  });
}

export function fetchCurrentUser(token: string): Promise<User> {
  return request<User>("/api/auth/me", {}, token);
}

export function fetchHealth(): Promise<{ message: string }> {
  return request<{ message: string }>("/");
}
