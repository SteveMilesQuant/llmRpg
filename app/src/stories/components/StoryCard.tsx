import { Divider, HStack, Heading, LinkOverlay, Text } from "@chakra-ui/react";
import { Link as RouterLink } from "react-router-dom";
import { Story } from "../Story";
import DeleteButton from "../../components/DeleteButton";
import CardContainer from "../../components/CardContainer";
import { useContext } from "react";
import PageContext, { PageContextType } from "../../pages/pageContext";

interface Props {
  story: Story;
  onDelete?: () => void;
}

const StoryCard = ({ story, onDelete }: Props) => {
  const pageContext = useContext(PageContext);
  const link =
    pageContext === PageContextType.public
      ? "/stories/" + story.id
      : "/design/" + story.id;

  return (
    <CardContainer>
      <HStack justifyContent="space-between">
        <LinkOverlay as={RouterLink} to={link}>
          <HStack alignItems="end">
            <Heading fontSize="2xl">{story.title}</Heading>
          </HStack>
        </LinkOverlay>
        {pageContext === PageContextType.design && onDelete && (
          <DeleteButton onConfirm={onDelete}>{story.title}</DeleteButton>
        )}
      </HStack>

      <Divider orientation="horizontal" marginTop={2} />
      <Text marginTop={2}>{story.blurb}</Text>
    </CardContainer>
  );
};

export default StoryCard;
