import { Divider, HStack, Heading, LinkOverlay, Text } from "@chakra-ui/react";
import { Link as RouterLink } from "react-router-dom";
import { Story } from "../Story";
import DeleteButton from "../../components/DeleteButton";
import CardContainer from "../../components/CardContainer";

interface Props {
  story: Story;
  onDelete?: () => void;
}

const StoryCard = ({ story, onDelete }: Props) => {
  return (
    <CardContainer>
      <HStack justifyContent="space-between">
        <LinkOverlay as={RouterLink} to={"/design/" + story.id}>
          <HStack alignItems="end">
            <Heading fontSize="2xl">{story.title}</Heading>
          </HStack>
        </LinkOverlay>
        {onDelete && (
          <DeleteButton onConfirm={onDelete}>{story.title}</DeleteButton>
        )}
      </HStack>

      <Divider orientation="horizontal" marginTop={2} />
      <Text marginTop={2}>{story.blurb}</Text>
    </CardContainer>
  );
};

export default StoryCard;
