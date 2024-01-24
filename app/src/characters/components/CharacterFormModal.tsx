import {
  Divider,
  Heading,
  Modal,
  ModalBody,
  ModalCloseButton,
  ModalContent,
  ModalFooter,
  ModalHeader,
  ModalOverlay,
} from "@chakra-ui/react";
import useCharacterForm from "../hooks/useCharacterForm";
import SubmitButton from "../../components/SubmitButton";
import CharacterFormBody from "./CharacterFormBody";

interface Props {
  title: string;
  isOpen: boolean;
  onClose: () => void;
  storyId: number;
}

const CharacterFormModal = ({ title, isOpen, onClose, storyId }: Props) => {
  const characterForm = useCharacterForm(storyId);

  return (
    <Modal
      isOpen={isOpen}
      onClose={() => {
        characterForm.handleClose();
        onClose();
      }}
      size="3xl"
    >
      <ModalOverlay />
      <ModalContent>
        <ModalHeader>
          <Heading fontSize="2xl">{title}</Heading>
          <Divider orientation="horizontal" marginTop={1}></Divider>
        </ModalHeader>
        <ModalCloseButton />
        <ModalBody>
          <CharacterFormBody {...characterForm} />
        </ModalBody>
        <ModalFooter>
          <SubmitButton
            onClick={() => {
              characterForm.handleSubmit();
              if (characterForm.isValid) {
                characterForm.handleClose();
                onClose();
              }
            }}
          >
            Submit
          </SubmitButton>
        </ModalFooter>
      </ModalContent>
    </Modal>
  );
};

export default CharacterFormModal;
