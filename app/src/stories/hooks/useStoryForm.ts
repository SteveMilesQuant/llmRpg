import { valibotResolver } from "@hookform/resolvers/valibot";
import { useMemo } from "react";
import { FieldValues, useForm } from "react-hook-form";
import { type Output, object, string, minLength } from "valibot";
import { Story } from "../Story";
import { useAddStory, useUpdateStory } from "./useStories";

export const storySchema = object({
  title: string([minLength(1, "Title is required.")]),
  setting: string(),
  blurb: string(),
});

export type FormData = Output<typeof storySchema>;

const useStoryForm = (story?: Story) => {
  const {
    register,
    control,
    handleSubmit: handleFormSubmit,
    formState: { errors, isValid },
    reset,
  } = useForm<FormData>({
    resolver: valibotResolver(storySchema),
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
