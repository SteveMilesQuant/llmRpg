import { useNavigate } from "react-router-dom";
import { Story } from "../Story";
import StoryFormBody from "./StoryFormBody";
import CrudButtonSet from "../../components/CrudButtonSet";
import { useDeleteStory } from "../hooks/useStories";
import useStoryForm from "../hooks/useStoryForm";
import { useState } from "react";

interface Props {
  story?: Story;
}

const StoryForm = ({ story }: Props) => {
  const navigate = useNavigate();
  const [isEditing, setIsEditing] = useState(false);
  const storyForm = useStoryForm(story);
  const deleteStory = useDeleteStory({
    onDelete: () => {
      navigate("/stories");
    },
  });

  const handleDelete = () => {
    if (story) deleteStory.mutate(story.id);
  };

  return (
    <>
      <StoryFormBody
        {...storyForm}
        isReadOnly={!isEditing}
        showLocation={true}
        storyId={story?.id}
      />
      <CrudButtonSet
        isEditing={isEditing}
        setIsEditing={setIsEditing}
        onDelete={handleDelete}
        confirmationLabel={story?.title}
        onCancel={storyForm.handleClose}
        onSubmit={storyForm.handleSubmit}
        isSubmitValid={storyForm.isValid}
      />
    </>
  );
};

export default StoryForm;
