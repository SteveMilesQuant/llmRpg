import {
  Modal,
  ModalBody,
  ModalCloseButton,
  ModalContent,
  ModalFooter,
  ModalHeader,
  ModalOverlay,
  Divider,
  Heading,
  HStack,
} from "@chakra-ui/react";
import StoryFormBody from "./StoryFormBody";
import useStoryForm from "../hooks/useStoryForm";
import CancelButton from "../../components/CancelButton";
import SubmitButton from "../../components/SubmitButton";

interface Props {
  title: string;
  isOpen: boolean;
  onClose: () => void;
}

const StoryFormModal = ({ title, isOpen, onClose }: Props) => {
  const storyForm = useStoryForm();

  return (
    <Modal
      isOpen={isOpen}
      onClose={() => {
        storyForm.handleClose();
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
          <StoryFormBody {...storyForm} showLocation={false} />
        </ModalBody>
        <ModalFooter>
          <HStack justifyContent="right" spacing={3}>
            <CancelButton onClick={onClose}>Cancel</CancelButton>
            <SubmitButton
              onClick={() => {
                storyForm.handleSubmit();
                if (storyForm.isValid) {
                  storyForm.handleClose();
                  onClose();
                }
              }}
            >
              Submit
            </SubmitButton>
          </HStack>
        </ModalFooter>
      </ModalContent>
    </Modal>
  );
};

export default StoryFormModal;
