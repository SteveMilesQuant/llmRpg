import { AiFillDelete } from "react-icons/ai";
import ActionButton from "./ActionButton";
import {
  Popover,
  PopoverArrow,
  PopoverBody,
  PopoverContent,
  PopoverHeader,
  PopoverTrigger,
  Button,
  HStack,
  Box,
  Heading,
  useDisclosure,
} from "@chakra-ui/react";
import CancelButton from "./CancelButton";

interface Props {
  children?: string; // name of the thing you want to delete
  onConfirm: () => void;
  disabled?: boolean;
}

const DeleteButton = ({ children, onConfirm, disabled }: Props) => {
  const { isOpen, onToggle, onClose } = useDisclosure();

  return (
    <Box>
      {/* Put popover in a box, to avoid warnings about it, when container might try to apply css*/}
      <Popover
        returnFocusOnClose={false}
        isOpen={isOpen}
        onClose={onClose}
        closeOnBlur={false}
      >
        <PopoverTrigger>
          <ActionButton
            Component={AiFillDelete}
            label="Delete"
            disabled={disabled}
            onClick={() => {
              if (!disabled) onToggle();
            }}
          />
        </PopoverTrigger>
        <PopoverContent>
          <PopoverArrow />
          <PopoverHeader>
            <Heading fontSize="md">
              Are you sure you want to remove {children}?
            </Heading>
          </PopoverHeader>
          <PopoverBody>
            <HStack justifyContent="right">
              <CancelButton onClick={onClose}>Cancel</CancelButton>
              <Button onClick={onConfirm} colorScheme="red">
                Delete
              </Button>
            </HStack>
          </PopoverBody>
        </PopoverContent>
      </Popover>
    </Box>
  );
};

export default DeleteButton;
