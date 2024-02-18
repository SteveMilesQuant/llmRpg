import {
  Input,
  Stack,
  CardBody,
  Card,
  Spinner,
  Text,
  Box,
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
import CharacterImage from "../characters/components/CharacterImage";

const Adventure = () => {
  const [playerName, setPlayerName] = useState("");
  const { data: adventure } = useAdventure();
  const addInteraction = useAddInteraction();
  const travel = useTravel();

  if (!adventure) return null;

  const isPending: boolean = addInteraction.isPending || travel.isPending;

  const allowCustomResponse =
    adventure.current_choices.length > 1 ||
    adventure.current_choices[0] != "BEGIN";

  return (
    <Stack spacing={5} marginX="auto">
      <AdventureTitle story_id={adventure.story_id} />
      {adventure.current_character_id && (
        <CharacterImage
          storyId={adventure.story_id}
          characterId={adventure.current_character_id}
        />
      )}
      {!isPending && adventure.current_narration === "" && (
        <Box bgColor="white" opacity="0.8">
          <Input
            type="text"
            placeholder="Enter your name..."
            onChange={(event) => setPlayerName(event.target.value)}
          />
        </Box>
      )}
      {!isPending && adventure.current_narration !== "" && (
        <Card opacity="0.8">
          <CardBody bgColor="brand.200" opacity="0.9" borderRadius={15}>
            <Text textColor="brand.100" fontSize={18} whiteSpace="pre-wrap">
              {adventure.current_narration}
            </Text>
          </CardBody>
        </Card>
      )}
      {!isPending && (
        <ChoicesCards
          playerName={playerName}
          choices={adventure.current_choices}
          addInteraction={addInteraction}
          allowCustomResponse={allowCustomResponse}
        />
      )}
      {!isPending && adventure.current_narration !== "" && (
        <TravelMenu story_id={adventure.story_id} travel={travel} />
      )}
      {isPending && (
        <Box width="fit-content" margin="auto">
          <Spinner marginX="auto" size="xl" />
        </Box>
      )}
    </Stack>
  );
};

export default Adventure;
