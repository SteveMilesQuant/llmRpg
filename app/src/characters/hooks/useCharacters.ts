import ms from "ms";
import APIClient from "../../services/api-client";
import APIHooks, {
  AddArgs,
  AddDataContext,
  DeleteArgs,
  DeleteDataContext,
  UpdateArgs,
  UpdateDataContext,
} from "../../services/api-hooks";
import { CACHE_KEY_CHARACTERS, Character, CharacterData } from "../Character";
import { CACHE_KEY_STORIES } from "../../stories";
import { UseMutationResult, UseQueryResult } from "@tanstack/react-query";

const useCharacterHooks = (storyId: number) =>
  new APIHooks<Character, CharacterData>(
    new APIClient<Character, CharacterData>(`/stories/${storyId}/characters`),
    [...CACHE_KEY_STORIES, storyId.toString(), ...CACHE_KEY_CHARACTERS],
    ms("5m")
  );

const useStoryCharacters = (storyId?: number) => {
  if (!storyId) return {} as UseQueryResult<Character[], Error>;
  const characterHooks = useCharacterHooks(storyId);
  return characterHooks.useDataList();
};
export default useStoryCharacters;

export const useAddCharacter = (
  storyId?: number,
  options?: AddArgs<Character, CharacterData>
) => {
  if (!storyId)
    return {} as UseMutationResult<
      Character,
      Error,
      CharacterData,
      AddDataContext<Character>
    >;
  const characterHooks = useCharacterHooks(storyId);
  return characterHooks.useAdd(options);
};

export const useUpdateCharacter = (
  storyId?: number,
  options?: UpdateArgs<Character>
) => {
  if (!storyId)
    return {} as UseMutationResult<
      Character,
      Error,
      Character,
      UpdateDataContext<Character>
    >;
  const characterHooks = useCharacterHooks(storyId);
  return characterHooks.useUpdate(options);
};

export const useDeleteCharacter = (
  storyId?: number,
  options?: DeleteArgs<Character>
) => {
  if (!storyId)
    return {} as UseMutationResult<
      any,
      Error,
      number,
      DeleteDataContext<Character>
    >;
  const characterHooks = useCharacterHooks(storyId);
  return characterHooks.useDelete(options);
};

export const useCharacter = (storyId?: number, characterId?: number) => {
  if (!storyId || !characterId) return {} as UseQueryResult<Character, Error>;
  const characterHooks = useCharacterHooks(storyId);
  return characterHooks.useData(characterId);
};

interface CharacterBaseImage {
  id: number;
  url: string;
}

const useCharacterImageHooks = (storyId: number, characterId: number) =>
  new APIHooks<CharacterBaseImage, undefined>(
    new APIClient<CharacterBaseImage, undefined>(
      `/stories/${storyId}/characters/${characterId}/base_image`
    ),
    [
      ...CACHE_KEY_STORIES,
      storyId.toString(),
      ...CACHE_KEY_CHARACTERS,
      characterId.toString(),
      "BASE_IMAGE",
    ],
    ms("5m")
  );

export const useCharacterBaseImage = (storyId: number, characterId: number) => {
  if (!storyId || !characterId)
    return {} as UseQueryResult<CharacterBaseImage, Error>;
  const imageHooks = useCharacterImageHooks(storyId, characterId);
  return imageHooks.useData();
};
