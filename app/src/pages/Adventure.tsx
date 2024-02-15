import {
  Input,
  Stack,
  CardBody,
  Card,
  Box,
  Spinner,
  Text,
} from "@chakra-ui/react";
import {
  useAddInteraction,
  useAdventure,
  useTravel,
} from "../hooks/useAdventure";
import { useState } from "react";
import ChoicesCards from "../components/ChoicesCards";
import TravelMenu from "../components/TravelMenu";
import AdventureTitle from "../components/AdventureTitle";

const Adventure = () => {
  const [playerName, setPlayerName] = useState("");
  const { data: adventure } = useAdventure();
  const addInteraction = useAddInteraction();
  const travel = useTravel();

  if (!adventure) return null;
  if (addInteraction.isPending || travel.isPending)
    return (
      <Box width="100%">
        <Spinner marginX="auto" size="xl" />
      </Box>
    );

  return (
    <Stack spacing={5} marginX="auto">
      <AdventureTitle story_id={adventure.story_id} />
      {adventure.current_narration === "" && (
        <Input
          type="text"
          placeholder="Enter your name..."
          onChange={(event) => setPlayerName(event.target.value)}
        />
      )}
      {adventure.current_narration !== "" && (
        <Card>
          <CardBody bgColor="brand.200">
            <Text textColor="brand.100" fontSize={18} whiteSpace="pre-wrap">
              {adventure.current_narration}
            </Text>
          </CardBody>
        </Card>
      )}
      <ChoicesCards
        playerName={playerName}
        choices={adventure.current_choices}
        addInteraction={addInteraction}
      />
      {adventure.current_narration !== "" && (
        <TravelMenu story_id={adventure.story_id} travel={travel} />
      )}
    </Stack>
  );
};

export default Adventure;
