import { Box, Button, HStack, Stack, useDisclosure } from "@chakra-ui/react";
import { useLocations } from "..";
import { useEffect, useState } from "react";
import { Location } from "..";
import LocationsMenu from "./LocationsMenu";
import LocationForm from "./LocationForm";
import LocationFormModal from "./LocationFormModal";

interface Props {
  storyId: number;
}

const Locations = ({ storyId }: Props) => {
  const { isOpen, onOpen, onClose } = useDisclosure();
  const [selectedLocation, setSelectedLocation] = useState<
    Location | undefined
  >(undefined);
  const { data: locations, error, isLoading } = useLocations(storyId);

  useEffect(() => {
    if (locations) setSelectedLocation(locations[0]);
  }, [!!locations]);

  if (isLoading) return null;
  if (error) throw error;

  return (
    <>
      <Stack spacing={5}>
        <HStack justifyContent="space-between">
          <LocationsMenu
            storyId={storyId}
            selectedLocation={selectedLocation}
            setSelectedLocation={setSelectedLocation}
          />
          <Button
            onClick={onOpen}
            bgColor={undefined}
            color="inherit"
            _hover={undefined}
          >
            Add location
          </Button>
        </HStack>
        <Box width="100%">
          {locations
            ?.filter((location) => location.id === selectedLocation?.id)
            .map((location) => (
              <LocationForm
                key={location.id}
                storyId={storyId}
                location={location}
              ></LocationForm>
            ))}
        </Box>
      </Stack>
      <LocationFormModal
        title="Add location"
        isOpen={isOpen}
        onClose={onClose}
        storyId={storyId}
        onSuccess={(newData: Location) => {
          setSelectedLocation(newData);
        }}
      ></LocationFormModal>
    </>
  );
};

export default Locations;
