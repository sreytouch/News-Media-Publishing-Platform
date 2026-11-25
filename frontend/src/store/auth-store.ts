import { create } from "zustand";

import { AuthUser } from "../types/models";

interface AuthState {
  accessToken: string | null;
  user: AuthUser | null;
  signIn: (payload: { accessToken: string; user: AuthUser }) => void;
  signOut: () => void;
}

const persistedToken = localStorage.getItem("nmpp.accessToken");
const persistedUser = localStorage.getItem("nmpp.user");

export const useAuthStore = create<AuthState>((set) => ({
  accessToken: persistedToken,
  user: persistedUser ? (JSON.parse(persistedUser) as AuthUser) : null,
  signIn: ({ accessToken, user }) => {
    localStorage.setItem("nmpp.accessToken", accessToken);
    localStorage.setItem("nmpp.user", JSON.stringify(user));
    set({ accessToken, user });
  },
  signOut: () => {
    localStorage.removeItem("nmpp.accessToken");
    localStorage.removeItem("nmpp.user");
    set({ accessToken: null, user: null });
  },
}));
