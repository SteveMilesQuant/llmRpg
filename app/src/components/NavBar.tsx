import { Box, HStack, Heading } from "@chakra-ui/react";
import SessionButton from "./SessionButton";

const NavBar = () => {
  return (
    <HStack
      justifyContent="space-between"
      width="100%"
      bgColor="brand.300"
      padding={2}
    >
      <Box padding={1} marginX={3}>
        <Heading fontFamily="monospace" fontSize="30px" color="brand.100">
          stories
        </Heading>
      </Box>
      <Box padding={1}>
        <SessionButton />
      </Box>
    </HStack>
  );
};

export default NavBar;
