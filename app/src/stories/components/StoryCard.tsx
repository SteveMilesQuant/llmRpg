import { Divider, HStack, Heading, LinkOverlay } from "@chakra-ui/react";
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
        <LinkOverlay as={RouterLink} to={"/stories/" + story.id}>
          <HStack alignItems="end">
            <Heading fontSize="2xl">{story.title}</Heading>
          </HStack>
        </LinkOverlay>
        {onDelete && (
          <DeleteButton onConfirm={onDelete}>{story.title}</DeleteButton>
        )}
      </HStack>

      <Divider orientation="horizontal" marginTop={2} />
      <HStack marginTop={2} justifyContent="space-between"></HStack>
    </CardContainer>
  );
};

export default StoryCard;
