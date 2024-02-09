import { UseMutationResult } from "@tanstack/react-query";
import {
  AddInteractionContext,
  Adventure,
  Choice,
} from "../hooks/useAdventure";
import CardContainer from "./CardContainer";

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
  return (
    <>
      {choices.map((choice) => (
        <CardContainer
          onClick={() => {
            addInteraction.mutate({
              player_name: playerName,
              choice: choice,
            } as Choice);
          }}
          key={choice}
        >
          {choice}
        </CardContainer>
      ))}
    </>
  );
};

export default ChoicesCards;
