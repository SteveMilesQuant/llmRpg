export interface StoryData {
  title: string;
  blurb: string;
  setting: string;
  is_published: boolean;
  starting_location_id: number;
}

export interface Story extends StoryData {
  id: number;
}

export const CACHE_KEY_STORIES = ["stories"];
