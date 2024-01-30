import { useEffect, useState } from "react";
import { axiosInstance } from "../../services/api-client";
import { create } from "zustand";

interface SessionStore {
  inProgress: boolean;
  expiration?: Date;
  start: (expiration: Date) => void;
  stop: () => void;
}

const useSessionStore = create<SessionStore>((set) => ({
  inProgress: false,
  expiration: undefined,
  start: (expiration: Date) => set(() => ({ inProgress: true, expiration })),
  stop: () => set(() => ({ inProgress: false })),
}));

const useSession = () => {
  const { inProgress, expiration, start, stop } = useSessionStore();
  const [isChecking, setIsChecking] = useState(true);

  // Check to see if we're already signed in
  useEffect(() => {
    const sessionToken = localStorage.getItem("sessionToken");
    const sessionExpiration = localStorage.getItem("sessionExpiration");
    if (sessionToken && sessionExpiration) {
      axiosInstance.defaults.headers.common = { Authorization: sessionToken };
      start(new Date(sessionExpiration + "Z"));
    }
    setIsChecking(false);
  }, []);

  const onStart = (storyId: number) => {
    axiosInstance.post("/start/" + storyId).then((response) => {
      localStorage.setItem("sessionToken", response.data.token);
      localStorage.setItem("sessionExpiration", response.data.expiration);
      axiosInstance.defaults.headers.common = {
        Authorization: response.data.token,
      };

      start(new Date(response.data.expiration + "Z"));
    });
  };

  const onRefresh = () => {
    axiosInstance.put("/refresh").then((response) => {
      localStorage.setItem("sessionToken", response.data.token);
      localStorage.setItem("sessionExpiration", response.data.expiration);
      axiosInstance.defaults.headers.common = {
        Authorization: response.data.token,
      };
      start(new Date(response.data.expiration + "Z"));
    });
  };

  const onStop = function () {
    axiosInstance.delete("/stop").then(() => {
      localStorage.removeItem("sessionToken");
      axiosInstance.defaults.headers.common = {};
      stop();
    });
  };

  return { inProgress, expiration, isChecking, onStart, onRefresh, onStop };
};

export default useSession;
