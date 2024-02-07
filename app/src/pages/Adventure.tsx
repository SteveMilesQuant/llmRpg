import { Box, Text } from "@chakra-ui/react";
import { useAdventure, useAddInteraction } from "../hooks/useAdventure";

const Adventure = () => {
  const { data: adventure } = useAdventure();
  const addInteraction = useAddInteraction({
    queryMutation: (newData, dataList) => {
      return dataList;
    },
  });

  if (!adventure) return;

  return (
    <Box>
      <Text>{adventure.current_narration}</Text>
      {adventure.current_choices.map((choice) => (
        <Box
          onClick={() => {
            addInteraction.mutate({ choice });
          }}
          key={choice}
        >
          {choice}
        </Box>
      ))}
    </Box>
  );
};

export default Adventure;
