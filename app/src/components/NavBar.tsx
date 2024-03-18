import { Box, HStack, Heading } from "@chakra-ui/react";
import SessionButton from "./SessionButton";
import { useContext } from "react";
import PageContext, { PageContextType } from "../pages/pageContext";
import AuthButton from "./AuthButton";

const NavBar = () => {
  const pageContextType = useContext(PageContext);

  return (
    <HStack justifyContent="space-between" width="100%" padding={2}>
      <Box padding={1} marginX={3}>
        <Heading
          fontFamily="monospace"
          fontSize="4xl"
          color="white"
          opacity="0.9"
        >
          {pageContextType === PageContextType.public ? "" : "design"}
        </Heading>
      </Box>
      <Box padding={1}>
        {pageContextType == PageContextType.public ? (
          <SessionButton />
        ) : (
          <AuthButton />
        )}
      </Box>
    </HStack>
  );
};

export default NavBar;
