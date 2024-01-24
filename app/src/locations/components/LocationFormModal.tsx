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
import useLocationForm from "../hooks/useLocationForm";
import SubmitButton from "../../components/SubmitButton";
import LocationFormBody from "./LocationFormBody";

interface Props {
  title: string;
  isOpen: boolean;
  onClose: () => void;
  storyId: number;
}

const LocationFormModal = ({ title, isOpen, onClose, storyId }: Props) => {
  const locationForm = useLocationForm(storyId);
  return (
    <Modal
      isOpen={isOpen}
      onClose={() => {
        locationForm.handleClose();
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
          <LocationFormBody {...locationForm} />
        </ModalBody>
        <ModalFooter>
          <SubmitButton
            onClick={() => {
              locationForm.handleSubmit();
              if (locationForm.isValid) {
                locationForm.handleClose();
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

export default LocationFormModal;
