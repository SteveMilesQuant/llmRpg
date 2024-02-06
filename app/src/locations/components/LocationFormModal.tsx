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
import { Location } from "..";

interface Props {
  title: string;
  isOpen: boolean;
  onClose: () => void;
  onSuccess?: (newData: Location) => void;
  storyId: number;
}

const LocationFormModal = ({
  title,
  isOpen,
  onClose,
  onSuccess,
  storyId,
}: Props) => {
  const locationForm = useLocationForm(storyId, undefined, onSuccess);

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
          <LocationFormBody {...locationForm} showStartingCharacter={false} />
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
