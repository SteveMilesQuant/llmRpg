import { SimpleGrid } from "@chakra-ui/react";
import StoryCard from "./StoryCard";
import { Story } from "../Story";

interface Props {
  stories: Story[];
}

const StoryGrid = ({ stories }: Props) => {
  return (
    <SimpleGrid>
      {stories.map((story) => (
        <StoryCard key={story.id} story={story} />
      ))}
    </SimpleGrid>
  );
};

export default StoryGrid;
