import { useEffect, useState } from "react";
import { axiosInstance } from "../../services/api-client";
import { create } from "zustand";
import { useQueryClient } from "@tanstack/react-query";

interface SessionStore {
  inProgress: boolean;
  start: () => void;
  stop: () => void;
}

const useSessionStore = create<SessionStore>((set) => ({
  inProgress: false,
  start: () => set(() => ({ inProgress: true })),
  stop: () => set(() => ({ inProgress: false })),
}));

const useSession = () => {
  const { inProgress, start, stop } = useSessionStore();
  const [isChecking, setIsChecking] = useState(true);
  const queryClient = useQueryClient();

  // Check to see if we're already signed in
  useEffect(() => {
    const sessionToken = localStorage.getItem("sessionToken");
    if (sessionToken) {
      axiosInstance.defaults.headers.common = { Authorization: sessionToken };
      start();
    }
    setIsChecking(false);
  }, []);

  const onStart = () => {
    axiosInstance.post("/start").then((token) => {
      localStorage.setItem("sessionToken", token.data);
      axiosInstance.defaults.headers.common = { Authorization: token.data };
      start();
    });
  };

  const onRefresh = () => {
    axiosInstance.put("/refresh").then((token) => {
      localStorage.setItem("sessionToken", token.data);
      axiosInstance.defaults.headers.common = { Authorization: token.data };
      start();
    });
  };

  const onStop = function () {
    localStorage.removeItem("sessionToken");
    axiosInstance.defaults.headers.common = {};
    queryClient.clear();
    stop();
  };

  return { inProgress, isChecking, onStart, onRefresh, onStop };
};

export default useSession;
