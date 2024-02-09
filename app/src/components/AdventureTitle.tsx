import { useStory } from "../stories";
import PageHeader from "./PageHeader";

interface Props {
  story_id: number;
}

const AdventureTitle = ({ story_id }: Props) => {
  const { data: story } = useStory(story_id);

  return <PageHeader hideUnderline={true}>{story?.title}</PageHeader>;
};

export default AdventureTitle;
