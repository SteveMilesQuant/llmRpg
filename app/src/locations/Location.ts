export interface LocationData {
  name: string;
  description: string;
  starting_character_id: number;
}

export interface Location extends LocationData {
  id: number;
}

export const CACHE_KEY_LOCATIONS = ["locations"];
