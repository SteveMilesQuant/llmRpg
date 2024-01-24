import ms from "ms";
import APIHooks from "../../services/api-hooks";
import APIClient from "../../services/api-client";
import { CACHE_KEY_STORIES, Story, StoryData } from "../Story";

export interface StoryQuery {
  is_published?: boolean;
  instructor_id?: number;
}

const storyHooks = new APIHooks<Story, StoryData>(
  new APIClient<Story, StoryData>("/stories"),
  CACHE_KEY_STORIES,
  ms("5m")
);

const useStories = (disabled: boolean) => {
  return storyHooks.useDataList(undefined, disabled);
};

export default useStories;
export const useStory = storyHooks.useData;
export const useAddStory = storyHooks.useAdd;
export const useUpdateStory = storyHooks.useUpdate;
export const useDeleteStory = storyHooks.useDelete;
