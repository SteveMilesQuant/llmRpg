export interface LocationData {
  name: string;
  description: string;
}

export interface Location extends LocationData {
  id: number;
}

export const CACHE_KEY_LOCATIONS = ["locations"];
