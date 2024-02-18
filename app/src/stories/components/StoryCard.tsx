import { Divider, HStack, Heading, Text } from "@chakra-ui/react";
import { Story } from "../Story";
import DeleteButton from "../../components/DeleteButton";
import CardContainer from "../../components/CardContainer";
import { useContext } from "react";
import PageContext, { PageContextType } from "../../pages/pageContext";
import useSession from "../../hooks/useSession";
import { useNavigate } from "react-router-dom";

interface Props {
  story: Story;
  onDelete?: () => void;
}

const StoryCard = ({ story, onDelete }: Props) => {
  const pageContext = useContext(PageContext);
  const navigate = useNavigate();
  const { onStart } = useSession(() => {
    navigate("/adventure");
  });

  return (
    <CardContainer
      onClick={() => {
        if (pageContext === PageContextType.public) {
          onStart(story.id);
        } else {
          navigate("/design/" + story.id);
        }
      }}
    >
      <HStack justifyContent="space-between">
        <HStack alignItems="end">
          <Heading
            fontSize="2xl"
            textColor="brand.300"
            fontFamily="Papyrus, fantasy"
          >
            {story.title}
          </Heading>
        </HStack>
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
