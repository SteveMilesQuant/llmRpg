import ms from "ms";
import APIClient from "../services/api-client";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

export const CACHE_KEY_ADVENTURES = ["adventures"];

export interface Adventure {
  id: number;
  story_id: number;
  current_narration: string;
  current_choices: string[];
}

export interface Choice {
  player_name: string;
  choice: string;
  location_id: number;
}

const adventureClient = new APIClient<Adventure>("/adventure");
const interactionClient = new APIClient<Adventure, Choice>("/interact");
const travelClient = new APIClient<Adventure, Choice>("/travel");

export const useAdventure = () => {
  return useQuery<Adventure, Error>({
    queryKey: CACHE_KEY_ADVENTURES,
    queryFn: () => adventureClient.get(),
    staleTime: ms("5m"),
  });
};

export interface AddInteractionContext {
  prevData: Adventure;
}

export const useAddInteraction = () => {
  const queryClient = useQueryClient();

  const addData = useMutation<Adventure, Error, Choice, AddInteractionContext>({
    mutationFn: (data: Choice) => interactionClient.post(data),
    onMutate: (newData: Choice) => {
      const prevData =
        queryClient.getQueryData<Adventure>(CACHE_KEY_ADVENTURES) ||
        ({} as Adventure);
      if (!newData) return; // this is silly, but npm run build is complaining about not using newData
      return { prevData };
    },
    onSuccess: (newData, submittedData) => {
      queryClient.setQueryData<Adventure>(CACHE_KEY_ADVENTURES, newData);
      if (!submittedData) return; // this is silly, but npm run build is complaining about not using newData
    },
    onError: (error, newData, context) => {
      if (!error || !context) return;
      queryClient.setQueryData<Adventure>(
        CACHE_KEY_ADVENTURES,
        () => context.prevData
      );
      if (!newData) return; // this is silly, but npm run build is complaining about not using newData
    },
  });

  return addData;
};

export const useTravel = () => {
  const queryClient = useQueryClient();

  const addData = useMutation<Adventure, Error, Choice, AddInteractionContext>({
    mutationFn: (data: Choice) => travelClient.post(data),
    onMutate: (newData: Choice) => {
      const prevData =
        queryClient.getQueryData<Adventure>(CACHE_KEY_ADVENTURES) ||
        ({} as Adventure);
      if (!newData) return; // this is silly, but npm run build is complaining about not using newData
      return { prevData };
    },
    onSuccess: (newData, submittedData) => {
      queryClient.setQueryData<Adventure>(CACHE_KEY_ADVENTURES, newData);
      if (!submittedData) return; // this is silly, but npm run build is complaining about not using newData
    },
    onError: (error, newData, context) => {
      if (!error || !context) return;
      queryClient.setQueryData<Adventure>(
        CACHE_KEY_ADVENTURES,
        () => context.prevData
      );
      if (!newData) return; // this is silly, but npm run build is complaining about not using newData
    },
  });

  return addData;
};
