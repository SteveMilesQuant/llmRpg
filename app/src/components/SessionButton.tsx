import { Box, Button, HStack, Text } from "@chakra-ui/react";
import { useSession } from "../users";
import { useNavigate } from "react-router-dom";

const SessionButton = () => {
  const { inProgress, onStop, onRefresh } = useSession();
  const navigate = useNavigate();

  return (
    <Box>
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
            onClick={() => {
              onStop();
              navigate("/");
            }}
          >
            <Text>Stop</Text>
          </Button>
        </HStack>
      )}
    </Box>
  );
};

export default SessionButton;
