import { valibotResolver } from "@hookform/resolvers/valibot";
import { useMemo } from "react";
import { FieldValues, useForm } from "react-hook-form";
import { type Output, object, string, minLength } from "valibot";
import { Character } from "../Character";
import { useAddCharacter, useUpdateCharacter } from "./useCharacters";

export const characterSchema = object({
  name: string([minLength(1, "Name is required.")]),
  description: string(),
});

export type FormData = Output<typeof characterSchema>;

const useCharacterForm = (
  storyId?: number,
  character?: Character,
  onSuccess?: (newData: Character) => void
) => {
  const {
    register,
    control,
    handleSubmit: handleFormSubmit,
    formState: { errors, isValid },
    reset,
  } = useForm<FormData>({
    resolver: valibotResolver(characterSchema),
    defaultValues: useMemo(() => {
      return {
        ...character,
      };
    }, [character]),
  });

  const addCharacter = useAddCharacter(storyId, { onSuccess });
  const updateCharacter = useUpdateCharacter(storyId);

  const handleClose = () => {
    reset({ ...character });
  };

  const handleSubmitLocal = (data: FieldValues) => {
    if (!storyId || !isValid) return;

    const newCharacter = {
      id: 0,
      ...character,
      ...data,
    } as Character;

    if (character) {
      // Update character
      updateCharacter.mutate(newCharacter);
    } else {
      // Add new character
      addCharacter.mutate(newCharacter);
    }
  };

  const handleSubmit = () => {
    handleFormSubmit(handleSubmitLocal)();
  };

  return {
    register,
    control,
    errors,
    handleClose,
    handleSubmit,
    isValid,
  };
};

export default useCharacterForm;
