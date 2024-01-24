import { Character, useCharacters } from "..";
import { Button, Menu, MenuButton, MenuItem, MenuList } from "@chakra-ui/react";
import { FaChevronDown } from "react-icons/fa";

interface Props {
  storyId: number;
  selectedCharacter?: Character;
  setSelectedCharacter: (character: Character | undefined) => void;
}

const CharactersMenu = ({
  storyId,
  selectedCharacter,
  setSelectedCharacter,
}: Props) => {
  const { data: characters, error, isLoading } = useCharacters(storyId);

  if (isLoading) return null;
  if (error) throw error;

  return (
    <Menu autoSelect={true}>
      <MenuButton as={Button} rightIcon={<FaChevronDown />}>
        {selectedCharacter?.name || "(none)"}
      </MenuButton>
      <MenuList>
        {characters?.map((character) => (
          <MenuItem
            key={character.id}
            onClick={() => setSelectedCharacter(character)}
          >
            {character.name}
          </MenuItem>
        ))}
      </MenuList>
    </Menu>
  );
};

export default CharactersMenu;
