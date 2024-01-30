import { Box, Button, HStack, Text } from "@chakra-ui/react";
import useSession from "../hooks/useSession";
import { useNavigate } from "react-router-dom";
import useCountdown from "../hooks/useCountdown";

const SessionButton = () => {
  const { inProgress, expiration, onStop, onRefresh } = useSession();
  const navigate = useNavigate();
  const { hours, minutes, seconds } = useCountdown(expiration);
  const hoursStr = hours < 10 ? "0" + hours : hours;
  const minStr = minutes < 10 ? "0" + minutes : minutes;
  const secStr = seconds < 10 ? "0" + seconds : seconds;

  return (
    <Box>
      {inProgress && (
        <HStack>
          <Box bgColor="white" padding={1} borderRadius="md">
            <Text>{hoursStr + ":" + minStr + ":" + secStr}</Text>
          </Box>
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
