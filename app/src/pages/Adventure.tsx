import { Box, Spinner, Input, Stack, CardBody, Card } from "@chakra-ui/react";
import { useAdventure, useAddInteraction } from "../hooks/useAdventure";
import BodyContainer from "../components/BodyContainer";
import CardContainer from "../components/CardContainer";
import { useState } from "react";
import PageHeader from "../components/PageHeader";
import { useStory } from "../stories";

const Adventure = () => {
  const [playerName, setPlayerName] = useState("");
  const { data: adventure } = useAdventure();
  const addInteraction = useAddInteraction();
  const { data: story } = useStory(adventure?.story_id);

  if (!adventure) return null;
  if (addInteraction.isPending)
    return (
      <BodyContainer>
        <Box width="100%">
          <Spinner marginX="auto" size="xl" />
        </Box>
      </BodyContainer>
    );

  return (
    <Stack spacing={5} marginX="auto">
      <PageHeader hideUnderline={true}>{story?.title}</PageHeader>
      {adventure.current_narration === "" && (
        <Input
          type="text"
          placeholder="Enter your name..."
          onChange={(event) => setPlayerName(event.target.value)}
        />
      )}
      {adventure.current_narration !== "" && (
        <Card>
          <CardBody textColor="brand.100" bgColor="brand.200" fontSize={18}>
            {adventure.current_narration}
          </CardBody>
        </Card>
      )}
      {adventure.current_choices.map((choice) => (
        <CardContainer
          onClick={() => {
            addInteraction.mutate({ player_name: playerName, choice: choice });
          }}
          key={choice}
        >
          {choice}
        </CardContainer>
      ))}
    </Stack>
  );
};

export default Adventure;
