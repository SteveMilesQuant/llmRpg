import { useParams } from "react-router-dom";
import PageHeader from "../components/PageHeader";
import { StoryTabs, useStory } from "../stories";

const Story = () => {
  const { id: idStr } = useParams();
  const id = idStr ? parseInt(idStr) : undefined;

  const { data: story, error, isLoading } = useStory(id);

  if (isLoading || !story) return null;
  if (error) throw error;

  return (
    <>
      <PageHeader hideUnderline={true}>{story?.title}</PageHeader>
      <StoryTabs story={story} />
    </>
  );
};

export default Story;
