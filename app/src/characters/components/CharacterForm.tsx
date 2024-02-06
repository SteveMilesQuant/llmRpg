import { useState } from "react";
import { Character, useDeleteCharacter } from "..";
import useCharacterForm from "../hooks/useCharacterForm";
import { useQueryClient } from "@tanstack/react-query";
import { CACHE_KEY_STORIES } from "../../stories";
import CrudButtonSet from "../../components/CrudButtonSet";
import CharacterFormBody from "./CharacterFormBody";

interface Props {
  storyId: number;
  character: Character;
}

const CharacterForm = ({ storyId, character }: Props) => {
  const [isEditing, setIsEditing] = useState(false);
  const queryClient = useQueryClient();
  const characterForm = useCharacterForm(storyId, character);
  const deleteCharacter = useDeleteCharacter(storyId, {
    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: CACHE_KEY_STORIES,
        exact: false,
      });
    },
  });

  const handleDelete = () => {
    deleteCharacter.mutate(character.id);
  };

  return (
    <>
      <CharacterFormBody
        {...characterForm}
        isReadOnly={!isEditing}
        showLocation={true}
        storyId={storyId}
      />
      <CrudButtonSet
        isEditing={isEditing}
        setIsEditing={setIsEditing}
        onDelete={handleDelete}
        confirmationLabel={character?.name}
        onCancel={characterForm.handleClose}
        onSubmit={characterForm.handleSubmit}
        isSubmitValid={characterForm.isValid}
      />
    </>
  );
};

export default CharacterForm;
