import { yupResolver } from "@hookform/resolvers/yup";
import { useMemo } from "react";
import { FieldValues, useForm } from "react-hook-form";
import { Location } from "../Location";
import { useAddLocation, useUpdateLocation } from "./useLocations";
import { object, string, number, InferType } from "yup";

export const locationSchema = object().shape({
  name: string().required(),
  description: string(),
  starting_character_id: number(),
});

export type FormData = InferType<typeof locationSchema>;

const useLocationForm = (
  storyId?: number,
  location?: Location,
  onSuccess?: (newData: Location) => void
) => {
  const {
    register,
    control,
    handleSubmit: handleFormSubmit,
    formState: { errors, isValid },
    reset,
  } = useForm<FormData>({
    resolver: yupResolver(locationSchema),
    defaultValues: useMemo(() => {
      return {
        ...location,
      };
    }, [location]),
  });

  const addLocation = useAddLocation(storyId, { onSuccess });
  const updateLocation = useUpdateLocation(storyId);

  const handleClose = () => {
    reset({ ...location });
  };

  const handleSubmitLocal = (data: FieldValues) => {
    if (!storyId || !isValid) return;

    const newLocation = {
      id: 0,
      ...location,
      ...data,
    } as Location;

    if (location) {
      // Update location
      updateLocation.mutate(newLocation);
    } else {
      // Add new location
      addLocation.mutate(newLocation);
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

export default useLocationForm;
