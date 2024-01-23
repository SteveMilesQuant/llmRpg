import { Button } from "@chakra-ui/react";
import { FormEvent } from "react";

interface Props {
  children: string;
  onClick: (e: FormEvent) => void;
  disabled?: boolean;
}

const CancelButton = ({ children, onClick, disabled }: Props) => {
  return (
    <Button
      onClick={onClick}
      disabled={disabled}
      bgColor={disabled ? "gray.100" : undefined}
      color={disabled ? "gray.200" : undefined}
      _hover={disabled ? { bgColor: "gray.100" } : undefined}
    >
      {children}
    </Button>
  );
};

export default CancelButton;
