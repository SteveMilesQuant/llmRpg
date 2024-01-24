import { Box, HStack, Heading, LinkOverlay } from "@chakra-ui/react";
import { Link as RouterLink } from "react-router-dom";
import AuthButton from "./AuthButton";

const AdminNavBar = () => {
  return (
    <HStack
      justifyContent="space-between"
      width="100%"
      bgColor="brand.300"
      padding={2}
    >
      <Box padding={1} marginX={3}>
        <LinkOverlay as={RouterLink} to={"/stories"}>
          <Heading fontFamily="monospace" fontSize="30px" color="brand.100">
            stories (admin)
          </Heading>
        </LinkOverlay>
      </Box>
      <Box padding={1}>
        <AuthButton />
      </Box>
    </HStack>
  );
};

export default AdminNavBar;
