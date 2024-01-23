import { Box, HStack } from "@chakra-ui/react";
import SessionButton from "./SessionButton";

const NavBar = () => {
  return (
    <>
      <Box
        width="100%"
        bgGradient="linear(to-b, brand.100, brand.300, brand.200)"
      >
        <HStack
          position="absolute"
          justifyContent="space-between"
          width="100%"
          padding={2}
        >
          <Box></Box>
          <Box padding={1}>
            <SessionButton />
          </Box>
        </HStack>
        <Box
          boxSize={{ base: "100px", lg: "300px" }}
          marginX="auto"
          paddingY={2}
        />
      </Box>
    </>
  );
};

export default NavBar;
