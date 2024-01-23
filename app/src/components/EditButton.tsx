import { AiFillEdit } from "react-icons/ai";
import ActionButton from "./ActionButton";

interface Props {
  isEditing: boolean;
  setIsEditing: (isEditing: boolean) => void;
}

const EditButton = ({ isEditing, setIsEditing }: Props) => {
  return (
    <ActionButton
      Component={AiFillEdit}
      label="Edit"
      onClick={() => setIsEditing(true)}
      disabled={isEditing}
    />
  );
};

export default EditButton;
