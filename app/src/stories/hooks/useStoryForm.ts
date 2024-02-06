import { yupResolver } from "@hookform/resolvers/yup";
import { useMemo } from "react";
import { FieldValues, useForm } from "react-hook-form";
import { Story } from "../Story";
import { useAddStory, useUpdateStory } from "./useStories";
import { object, string, number, InferType } from "yup";

export const storySchema = object().shape({
  title: string().required(),
  setting: string(),
  blurb: string(),
  starting_location_id: number(),
});

export type FormData = InferType<typeof storySchema>;

const useStoryForm = (story?: Story) => {
  const {
    register,
    control,
    handleSubmit: handleFormSubmit,
    formState: { errors, isValid },
    reset,
  } = useForm<FormData>({
    resolver: yupResolver(storySchema),
    defaultValues: useMemo(() => {
      return {
        ...story,
      };
    }, [story]),
  });

  const addStory = useAddStory();
  const updateStory = useUpdateStory();

  const handleClose = () => {
    reset({ ...story });
  };

  const handleSubmitLocal = (data: FieldValues) => {
    if (!isValid) return;

    const newStory = {
      id: 0,
      ...story,
      ...data,
    } as Story;

    if (story) {
      // Update story
      updateStory.mutate(newStory);
    } else {
      // Add new story
      addStory.mutate(newStory);
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

export default useStoryForm;
