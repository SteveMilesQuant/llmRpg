import { Box, Button, HStack, Text } from "@chakra-ui/react";
import { useSession } from "../users";

const SessionButton = () => {
  const { inProgress, onStart, onStop, onRefresh } = useSession();

  return (
    <Box>
      {!inProgress && (
        <Button
          variant="outline"
          bgColor="white"
          textColor="brand.100"
          size="sm"
          onClick={() => onStart()}
        >
          Start
        </Button>
      )}
      {inProgress && (
        <HStack>
          <Button
            variant="outline"
            bgColor="white"
            textColor="brand.100"
            size="sm"
            onClick={() => onRefresh()}
          >
            <Text>Refresh</Text>
          </Button>
          <Button
            variant="outline"
            bgColor="white"
            textColor="brand.100"
            size="sm"
            onClick={() => onStop()}
          >
            <Text>Stop</Text>
          </Button>
        </HStack>
      )}
    </Box>
  );
};

export default SessionButton;
