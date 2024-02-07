import ms from "ms";
import APIClient from "../services/api-client";
import APIHooks from "../services/api-hooks";

const CACHE_KEY_ADVENTURES = ["adventures"];

interface Adventure {
  id: number;
  current_narration: string;
  current_choices: string[];
}

interface Choice {
  choice: string;
}

const adventureHooks = new APIHooks<Adventure>(
  new APIClient<Adventure>("/adventure"),
  CACHE_KEY_ADVENTURES,
  ms("5m")
);

const interactionHooks = new APIHooks<Adventure, Choice>(
  new APIClient<Adventure, Choice>("/interact"),
  CACHE_KEY_ADVENTURES, // yes, use the same key here
  ms("5m")
);

export const useAdventure = adventureHooks.useData;
export const useAddInteraction = interactionHooks.useAdd;
