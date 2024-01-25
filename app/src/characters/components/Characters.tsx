import { Box, Button, HStack, Stack, useDisclosure } from "@chakra-ui/react";
import { useCharacters } from "..";
import { useEffect, useState } from "react";
import { Character } from "..";
import CharactersMenu from "./CharacterssMenu";
import CharacterForm from "./CharacterForm";
import CharacterFormModal from "./CharacterFormModal";

interface Props {
  storyId: number;
}

const Characters = ({ storyId }: Props) => {
  const { isOpen, onOpen, onClose } = useDisclosure();
  const [selectedCharacter, setSelectedCharacter] = useState<
    Character | undefined
  >(undefined);
  const { data: characters, error, isLoading } = useCharacters(storyId);

  useEffect(() => {
    if (characters) setSelectedCharacter(characters[0]);
  }, [!!characters]);

  if (isLoading) return null;
  if (error) throw error;

  return (
    <>
      <Stack spacing={5}>
        <HStack justifyContent="space-between">
          <CharactersMenu
            storyId={storyId}
            selectedCharacter={selectedCharacter}
            setSelectedCharacter={setSelectedCharacter}
          />
          <Button
            onClick={onOpen}
            bgColor={undefined}
            color="inherit"
            _hover={undefined}
          >
            Add character
          </Button>
        </HStack>
        <Box width="100%">
          {characters
            ?.filter((character) => character.id === selectedCharacter?.id)
            .map((character) => (
              <CharacterForm
                key={character.id}
                storyId={storyId}
                character={character}
              ></CharacterForm>
            ))}
        </Box>
      </Stack>
      <CharacterFormModal
        title="Add character"
        isOpen={isOpen}
        onClose={onClose}
        storyId={storyId}
        onSuccess={(newData: Character) => {
          setSelectedCharacter(newData);
        }}
      ></CharacterFormModal>
    </>
  );
};

export default Characters;
