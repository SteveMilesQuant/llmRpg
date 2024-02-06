export interface CharacterData {
  name: string;
  public_description: string;
  private_description: string;
  location_id: number;
}

export interface Character extends CharacterData {
  id: number;
}

export const CACHE_KEY_CHARACTERS = ["characters"];
