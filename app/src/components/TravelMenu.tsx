import { Menu, MenuButton, Button, MenuList, MenuItem } from "@chakra-ui/react";
import { useLocations } from "../locations";
import {
  AddInteractionContext,
  Adventure,
  Choice,
} from "../hooks/useAdventure";
import { UseMutationResult } from "@tanstack/react-query";

interface Props {
  story_id: number;
  travel: UseMutationResult<Adventure, Error, Choice, AddInteractionContext>;
}

const TravelMenu = ({ story_id, travel }: Props) => {
  const { data: locations } = useLocations(story_id);

  return (
    <Menu>
      <MenuButton as={Button} textColor="brand.100">
        Travel
      </MenuButton>
      <MenuList>
        {locations?.map((location) => (
          <MenuItem
            key={location.id}
            onClick={() =>
              travel.mutate({
                location_id: location.id,
              } as Choice)
            }
          >
            {location.name}
          </MenuItem>
        ))}
      </MenuList>
    </Menu>
  );
};

export default TravelMenu;
