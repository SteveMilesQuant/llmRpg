import { useEffect, useState } from "react";
import useSession from "./useSession";
import { axiosInstance } from "../services/api-client";

interface StoryQueryData {
  user_response: string;
}

const useStoryQuery = () => {
  const { inProgress } = useSession();
  const [narratorResponse, setNarratorResponse] = useState("");

  useEffect(() => {
    if (inProgress) {
      axiosInstance
        .post("/query", { user_response: "" } as StoryQueryData)
        .then((response) => {
          setNarratorResponse(response.data);
        });
    }
  }, [inProgress]);

  return { narratorResponse };
};

export default useStoryQuery;
