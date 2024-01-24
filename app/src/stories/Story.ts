export interface StoryData {
  title: string;
  setting: string;
}

export interface Story extends StoryData {
  id: number;
}

export const CACHE_KEY_STORIES = ["stories"];
