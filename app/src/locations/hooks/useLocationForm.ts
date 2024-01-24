import { valibotResolver } from "@hookform/resolvers/valibot";
import { useMemo } from "react";
import { FieldValues, useForm } from "react-hook-form";
import { type Output, object, string, minLength } from "valibot";
import { Location } from "../Location";
import { useAddLocation, useUpdateLocation } from "./useLocations";

export const locationSchema = object({
  name: string([minLength(1, "Name is required.")]),
  description: string(),
});

export type FormData = Output<typeof locationSchema>;

const useLocationForm = (storyId?: number, location?: Location) => {
  const {
    register,
    control,
    handleSubmit: handleFormSubmit,
    formState: { errors, isValid },
    reset,
  } = useForm<FormData>({
    resolver: valibotResolver(locationSchema),
    defaultValues: useMemo(() => {
      return {
        ...location,
      };
    }, [location]),
  });

  const addLocation = useAddLocation(storyId);
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
