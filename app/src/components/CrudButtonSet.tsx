import { HStack } from "@chakra-ui/react";
import CancelButton from "./CancelButton";
import DeleteButton from "./DeleteButton";
import EditButton from "./EditButton";
import SubmitButton from "./SubmitButton";

interface Props {
  isEditing: boolean;
  setIsEditing: (isEditing: boolean) => void;
  onDelete?: () => void;
  confirmationLabel?: string;
  onCancel: () => void;
  onSubmit: () => void;
  isSubmitValid: boolean;
}

const CrudButtonSet = ({
  isEditing,
  setIsEditing,
  onDelete,
  confirmationLabel,
  onCancel,
  onSubmit,
  isSubmitValid,
}: Props) => {
  return (
    <HStack justifyContent="right" spacing={3} paddingTop={3}>
      {onDelete && (
        <DeleteButton onConfirm={onDelete} disabled={isEditing}>
          {confirmationLabel}
        </DeleteButton>
      )}
      <EditButton isEditing={isEditing} setIsEditing={setIsEditing} />
      <CancelButton
        onClick={() => {
          onCancel();
          setIsEditing(false);
        }}
        disabled={!isEditing}
      >
        Cancel
      </CancelButton>
      <SubmitButton
        onClick={() => {
          if (isSubmitValid) {
            setIsEditing(false);
            onSubmit();
          }
        }}
        disabled={!isEditing}
      >
        Update
      </SubmitButton>
    </HStack>
  );
};

export default CrudButtonSet;
