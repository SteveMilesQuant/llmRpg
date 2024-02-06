import { yupResolver } from "@hookform/resolvers/yup";
import { useMemo } from "react";
import { FieldValues, useForm } from "react-hook-form";
import { object, string, number, InferType } from "yup";
import { Character } from "../Character";
import { useAddCharacter, useUpdateCharacter } from "./useCharacters";

export const characterSchema = object().shape({
  name: string().required(),
  public_description: string(),
  private_description: string(),
  location_id: number(),
});

export type FormData = InferType<typeof characterSchema>;

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
    resolver: yupResolver(characterSchema),
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
