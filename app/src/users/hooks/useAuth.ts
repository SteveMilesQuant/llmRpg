import { useEffect, useState } from "react";
import {
  TokenResponse,
  googleLogout,
  useGoogleLogin,
} from "@react-oauth/google";
import { axiosInstance } from "../../services/api-client";
import { create } from "zustand";
import { mountStoreDevtool } from "simple-zustand-devtools";
import { useQueryClient } from "@tanstack/react-query";

interface UserStore {
  signedIn: boolean;
  login: () => void;
  logout: () => void;
}

const useUserStore = create<UserStore>((set) => ({
  signedIn: false,
  login: () => set(() => ({ signedIn: true })),
  logout: () => set(() => ({ signedIn: false })),
}));

if (process.env.NODE_ENV === "development")
  mountStoreDevtool("Counter store", useUserStore);

const useAuth = () => {
  const { signedIn, login, logout } = useUserStore();
  const [isChecking, setIsChecking] = useState(true);
  const queryClient = useQueryClient();

  // Check to see if we're already signed in
  useEffect(() => {
    const authToken = localStorage.getItem("authToken");
    if (authToken) {
      axiosInstance.defaults.headers.common = { Authorization: authToken };
      login();
    }
    setIsChecking(false);
  }, []);

  const apiSignIn = (
    codeResponse: Omit<
      TokenResponse,
      "error" | "error_description" | "error_uri"
    >
  ) => {
    axiosInstance.post("/signin", codeResponse).then((response) => {
      localStorage.setItem("authToken", response.data.token);
      axiosInstance.defaults.headers.common = {
        Authorization: response.data.token,
      };
      login();
    });
  };

  const googleLogin = useGoogleLogin({
    onSuccess: (codeResponse) => apiSignIn(codeResponse),
    onError: (error) => {
      throw error;
    },
  });

  const onLogout = function () {
    googleLogout();
    localStorage.removeItem("authToken");
    axiosInstance.defaults.headers.common = {};
    queryClient.clear();
    logout();
  };

  return { signedIn, isChecking, onLogin: googleLogin, onLogout };
};

export default useAuth;
