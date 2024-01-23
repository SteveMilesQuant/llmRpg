import { Divider, HStack, Heading } from "@chakra-ui/react";
import { ReactNode } from "react";

interface Props {
  rightButton?: ReactNode;
  children?: string;
  hideUnderline?: boolean;
  fontSize?: string;
}

const PageHeader = ({
  rightButton,
  children,
  hideUnderline,
  fontSize,
}: Props) => {
  return (
    <>
      <HStack justifyContent="space-between" marginBottom={5}>
        <Heading fontSize={fontSize || "3xl"}>{children}</Heading>
        {rightButton}
      </HStack>
      {!hideUnderline && <Divider orientation="horizontal" marginY={5} />}
    </>
  );
};

export default PageHeader;
