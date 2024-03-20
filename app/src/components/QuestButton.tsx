import { useDisclosure } from "@chakra-ui/react";
import { useAdventure } from "../hooks/useAdventure";
import QuestModal from "./QuestModal";
import ActionButton from "./ActionButton";
import { AiTwotoneFlag } from "react-icons/ai";

const QuestButton = () => {
  const { data: adventure } = useAdventure();
  const { isOpen, onClose, onToggle } = useDisclosure();

  if (!adventure || !adventure.quests || adventure.quests.length === 0)
    return null;

  return (
    <>
      <ActionButton
        Component={AiTwotoneFlag}
        label="Quests"
        onClick={onToggle}
      />
      <QuestModal quests={adventure.quests} isOpen={isOpen} onClose={onClose} />
    </>
  );
};

export default QuestButton;
