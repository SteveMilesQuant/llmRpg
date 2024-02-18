import { Divider, HStack, Heading, Box } from "@chakra-ui/react";
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
        <Box borderRadius={15} padding={3} bgColor="rgba(255,255,255,0.8)">
          <Heading
            fontSize={fontSize || "3xl"}
            textColor="brand.300"
            fontFamily="Papyrus, fantasy"
          >
            {children}
          </Heading>
        </Box>
        {rightButton}
      </HStack>
      {!hideUnderline && <Divider orientation="horizontal" marginY={5} />}
    </>
  );
};

export default PageHeader;
