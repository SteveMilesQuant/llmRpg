import { Tooltip } from "@chakra-ui/react";
import { ReactNode } from "react";

interface Props {
  children: ReactNode;
  label?: string;
  isOpen: boolean;
}

const InputError = ({ children, label, isOpen }: Props) => {
  return (
    <Tooltip
      label={label}
      isOpen={isOpen}
      hasArrow
      bg="red.500"
      placement="top"
      gutter={9}
    >
      {children}
    </Tooltip>
  );
};

export default InputError;
