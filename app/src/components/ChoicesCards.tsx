import { UseMutationResult } from "@tanstack/react-query";
import {
  AddInteractionContext,
  Adventure,
  Choice,
} from "../hooks/useAdventure";
import CardContainer from "./CardContainer";
import { Box, IconButton, Input } from "@chakra-ui/react";
import { useState } from "react";
import { FaArrowRightFromBracket } from "react-icons/fa6";

interface Props {
  playerName: string;
  choices: string[];
  addInteraction: UseMutationResult<
    Adventure,
    Error,
    Choice,
    AddInteractionContext
  >;
}

const ChoicesCards = ({ playerName, choices, addInteraction }: Props) => {
  const [customResponse, setCustomResponse] = useState("");

  return (
    <>
      {choices.map((choice) => (
        <CardContainer
          onClick={() =>
            addInteraction.mutate({
              player_name: playerName,
              choice: choice,
            } as Choice)
          }
          key={choice}
        >
          {choice}
        </CardContainer>
      ))}
      <Box>
        <Input
          placeholder="Custom response..."
          onChange={(event) => setCustomResponse(event.target.value)}
        />
        <IconButton
          icon={<FaArrowRightFromBracket />}
          aria-label="Submit custom response"
          position="absolute"
          right={5}
          marginRight={3}
          bgColor="white"
          borderColor="gray.200"
          borderStyle="solid"
          borderWidth={1}
          borderRadius={6}
          zIndex={1}
          onClick={() =>
            addInteraction.mutate({
              player_name: playerName,
              choice: customResponse,
            } as Choice)
          }
        />
      </Box>
    </>
  );
};

export default ChoicesCards;
