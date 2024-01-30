import ms from "ms";
import APIHooks from "../../services/api-hooks";
import APIClient from "../../services/api-client";
import { CACHE_KEY_STORIES, Story, StoryData } from "../Story";

export interface StoryQuery {
  is_published?: boolean;
}

const storyHooks = new APIHooks<Story, StoryData>(
  new APIClient<Story, StoryData>("/stories"),
  CACHE_KEY_STORIES,
  ms("5m")
);

const useStories = (storyQuery: StoryQuery, disabled: boolean) => {
  return storyHooks.useDataList(
    Object.keys(storyQuery).length ? { params: { ...storyQuery } } : undefined,
    disabled
  );
};

export default useStories;
export const useStory = storyHooks.useData;
export const useAddStory = storyHooks.useAdd;
export const useUpdateStory = storyHooks.useUpdate;
export const useDeleteStory = storyHooks.useDelete;
