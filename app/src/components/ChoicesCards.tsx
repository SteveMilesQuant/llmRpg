import CardContainer from "./CardContainer";
import { Box, IconButton, Input } from "@chakra-ui/react";
import { useState } from "react";
import { FaArrowRightFromBracket } from "react-icons/fa6";

interface Props {
  choices: string[];
  onSubmit: (choice: string) => void;
}

const ChoicesCards = ({ choices, onSubmit }: Props) => {
  const [customResponse, setCustomResponse] = useState("");

  return (
    <>
      {choices.map((choice) => (
        <CardContainer onClick={() => onSubmit(choice)} key={choice}>
          {choice}
        </CardContainer>
      ))}
      <Box>
        <Input
          placeholder="Custom response..."
          onChange={(event) => setCustomResponse(event.target.value)}
          bgColor="white"
          opacity="0.8"
        />
        <IconButton
          icon={<FaArrowRightFromBracket />}
          aria-label="Submit custom response"
          position="absolute"
          right={5}
          marginRight={3}
          bgColor="white"
          opacity="0.8"
          borderColor="gray.200"
          borderStyle="solid"
          borderWidth={1}
          borderRadius={6}
          zIndex={1}
          onClick={() => onSubmit(customResponse)}
        />
      </Box>
    </>
  );
};

export default ChoicesCards;
