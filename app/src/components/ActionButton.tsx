import { IconButton, forwardRef } from "@chakra-ui/react";
import { IconType } from "react-icons/lib";

interface Props {
  Component: IconType;
  onClick?: () => void;
  label: string;
  disabled?: boolean;
}

const ActionButton = forwardRef(
  ({ Component, onClick, label, disabled }: Props, ref) => {
    return (
      <IconButton
        icon={<Component size="18px" />}
        aria-label={label}
        size="sm"
        variant="ghost"
        onClick={onClick}
        ref={ref}
        disabled={disabled}
        color={disabled ? "gray.100" : undefined}
        _hover={disabled ? { bgColor: "transparent" } : undefined}
      />
    );
  }
);

export default ActionButton;
