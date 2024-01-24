import { Location, useLocations } from "..";
import { Button, Menu, MenuButton, MenuItem, MenuList } from "@chakra-ui/react";
import { FaChevronDown } from "react-icons/fa";

interface Props {
  storyId: number;
  selectedLocation?: Location;
  setSelectedLocation: (location: Location | undefined) => void;
}

const LocationsMenu = ({
  storyId,
  selectedLocation,
  setSelectedLocation,
}: Props) => {
  const { data: locations, error, isLoading } = useLocations(storyId);

  if (isLoading) return null;
  if (error) throw error;

  return (
    <Menu autoSelect={true}>
      <MenuButton as={Button} rightIcon={<FaChevronDown />}>
        {selectedLocation?.name || "(none)"}
      </MenuButton>
      <MenuList>
        {locations?.map((location) => (
          <MenuItem
            key={location.id}
            onClick={() => setSelectedLocation(location)}
          >
            {location.name}
          </MenuItem>
        ))}
      </MenuList>
    </Menu>
  );
};

export default LocationsMenu;
