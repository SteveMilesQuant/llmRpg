import { useState } from "react";
import { Location, useDeleteLocation } from "..";
import useLocationForm from "../hooks/useLocationForm";
import { useQueryClient } from "@tanstack/react-query";
import { CACHE_KEY_STORIES } from "../../stories";
import CrudButtonSet from "../../components/CrudButtonSet";
import LocationFormBody from "./LocationFormBody";

interface Props {
  storyId: number;
  location: Location;
}

const LocationForm = ({ storyId, location }: Props) => {
  const [isEditing, setIsEditing] = useState(false);
  const queryClient = useQueryClient();
  const locationForm = useLocationForm(storyId, location);
  const deleteLocation = useDeleteLocation(storyId, {
    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: CACHE_KEY_STORIES,
        exact: false,
      });
    },
  });

  const handleDelete = () => {
    deleteLocation.mutate(location.id);
  };

  return (
    <>
      <LocationFormBody
        {...locationForm}
        isReadOnly={!isEditing}
        showStartingCharacter={true}
        storyId={storyId}
      />
      <CrudButtonSet
        isEditing={isEditing}
        setIsEditing={setIsEditing}
        onDelete={handleDelete}
        confirmationLabel={location?.name}
        onCancel={locationForm.handleClose}
        onSubmit={locationForm.handleSubmit}
        isSubmitValid={locationForm.isValid}
      />
    </>
  );
};

export default LocationForm;
