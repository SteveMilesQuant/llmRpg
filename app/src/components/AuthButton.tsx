import { Box, Button, Text } from "@chakra-ui/react";
import { FcGoogle } from "react-icons/fc";
import { useAuth } from "../users";

const AuthButton = () => {
  const { signedIn, onLogin, onLogout } = useAuth();

  return (
    <Box>
      {!signedIn && (
        <Button
          leftIcon={<FcGoogle />}
          variant="outline"
          bgColor="white"
          textColor="brand.100"
          size="sm"
          onClick={() => onLogin()}
        >
          Sign In
        </Button>
      )}
      {signedIn && (
        <Button
          variant="outline"
          bgColor="white"
          textColor="brand.100"
          size="sm"
          onClick={() => onLogout()}
        >
          <Text>Sign Out</Text>
        </Button>
      )}
    </Box>
  );
};

export default AuthButton;
