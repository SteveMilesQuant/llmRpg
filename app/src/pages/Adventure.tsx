import { Stack, CardBody, Card, Text } from "@chakra-ui/react";
import {
  Choice,
  useAddInteraction,
  useAdventure,
  useTravel,
} from "../hooks/useAdventure";
import ChoicesCards from "../components/ChoicesCards";
import TravelMenu from "../components/TravelMenu";
import AdventureTitle from "../components/AdventureTitle";
import CharacterImage from "../characters/components/CharacterImage";
import AdventureSkeleton from "../components/AdventureSkeleton";

const Adventure = () => {
  const { data: adventure } = useAdventure();
  const addInteraction = useAddInteraction();
  const travel = useTravel();

  if (!adventure) return null;

  const isPending: boolean = addInteraction.isPending || travel.isPending;

  // If the adventure is underway, submit reponse as interaction
  // Otherwise, submit it as "travel" (i.e. "embarking" is considered "travel")
  // Player_name is the indicator of whether we are underway or not
  const onSubmitChoice = !!adventure.player_name
    ? (choice: string) => addInteraction.mutate({ choice: choice } as Choice)
    : (choice: string) => travel.mutate({ choice: choice } as Choice);

  return (
    <Stack spacing={5} marginX="auto">
      <AdventureTitle story_id={adventure.story_id} />
      {adventure.current_character_id && (
        <CharacterImage
          storyId={adventure.story_id}
          characterId={adventure.current_character_id}
        />
      )}
      {isPending && <AdventureSkeleton />}
      {!isPending && (
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
          choices={adventure.current_choices}
          onSubmit={onSubmitChoice}
        />
      )}
      {adventure.current_character_id && !isPending && (
        <TravelMenu story_id={adventure.story_id} travel={travel} />
      )}
    </Stack>
  );
};

export default Adventure;
