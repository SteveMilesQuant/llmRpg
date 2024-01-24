export interface CharacterData {
  name: string;
  description: string;
}

export interface Character extends CharacterData {
  id: number;
}

export const CACHE_KEY_CHARACTERS = ["characters"];
