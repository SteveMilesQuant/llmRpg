import { SimpleGrid } from "@chakra-ui/react";
import StoryCard from "./StoryCard";
import { Story } from "../Story";
import { useDeleteStory } from "..";

interface Props {
  stories: Story[];
}

const StoryGrid = ({ stories }: Props) => {
  const deleteStory = useDeleteStory();
  return (
    <SimpleGrid>
      {stories.map((story) => (
        <StoryCard
          key={story.id}
          story={story}
          onDelete={() => deleteStory.mutate(story.id)}
        />
      ))}
    </SimpleGrid>
  );
};

export default StoryGrid;
