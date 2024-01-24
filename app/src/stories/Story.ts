export interface StoryData {
  title: string;
  description: string;
}

export interface Story extends StoryData {
  id: number;
}

export const CACHE_KEY_STORIES = ["stories"];
