import {
  ListItem,
  Modal,
  ModalBody,
  ModalCloseButton,
  ModalContent,
  ModalHeader,
  ModalOverlay,
  UnorderedList,
} from "@chakra-ui/react";
import { Quest } from "../hooks/useAdventure";

interface Props {
  quests: Quest[];
  isOpen: boolean;
  onClose: () => void;
}

const QuestModal = ({ quests, isOpen, onClose }: Props) => {
  return (
    <Modal isOpen={isOpen} onClose={onClose} size="sm">
      <ModalOverlay />
      <ModalContent bgColor="white">
        <ModalHeader>Quests</ModalHeader>
        <ModalCloseButton />
        <ModalBody>
          <UnorderedList>
            {quests.map((q) => (
              <ListItem
                key={q.id}
                textDecor={
                  q.achieved_count >= q.target_count
                    ? "line-through"
                    : undefined
                }
              >
                {!q.accepted && "(Pending) "}
                {q.target_behavior}
              </ListItem>
            ))}
          </UnorderedList>
        </ModalBody>
      </ModalContent>
    </Modal>
  );
};

export default QuestModal;
