import { Box, Button, HStack, Text } from "@chakra-ui/react";
import { useSession } from "../users";
import { useNavigate } from "react-router-dom";
import { useEffect, useRef, useState } from "react";

const SessionButton = () => {
  const { inProgress, expiration, onStop, onRefresh } = useSession();
  const navigate = useNavigate();
  const Ref = useRef<NodeJS.Timeout | null>(null);

  // The state for our timer
  const [timer, setTimer] = useState("00:00:00");

  const getTimeRemaining = (e: Date) => {
    const today = new Date();
    const total = e.getTime() - today.getTime();
    const seconds = Math.floor((total / 1000) % 60);
    const minutes = Math.floor((total / 1000 / 60) % 60);
    const hours = Math.floor((total / 1000 / 60 / 60) % 24);
    return {
      total,
      hours,
      minutes,
      seconds,
    };
  };

  const startTimer = (e: Date) => {
    let { total, hours, minutes, seconds } = getTimeRemaining(e);
    if (total >= 0) {
      // update the timer
      // check if less than 10 then we need to
      // add '0' at the beginning of the variable
      setTimer(
        (hours > 9 ? hours : "0" + hours) +
          ":" +
          (minutes > 9 ? minutes : "0" + minutes) +
          ":" +
          (seconds > 9 ? seconds : "0" + seconds)
      );
    }
  };

  const clearTimer = (e: Date) => {
    // If you try to remove this line the
    // updating of timer Variable will be
    // after 1000ms or 1sec
    if (Ref.current) clearInterval(Ref.current);
    const id = setInterval(() => {
      startTimer(e);
    }, 1000);
    Ref.current = id;
  };

  useEffect(() => {
    if (expiration) clearTimer(expiration);
  }, [expiration]);

  return (
    <Box>
      {inProgress && (
        <HStack>
          <Text>{timer}</Text>
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
