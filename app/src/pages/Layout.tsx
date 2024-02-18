import { Outlet } from "react-router-dom";
import { HStack, Box } from "@chakra-ui/react";
import NavBar from "../components/NavBar";
import { ReactNode } from "react";
import BodyContainer from "../components/BodyContainer";
import bgImage from "../assets/mainpagebgimage.png";

interface Props {
  children?: ReactNode;
}

const Layout = ({ children }: Props) => {
  // Include both Outlet and children, to allow both contexts

  return (
    <Box width="100vw" bgImage={bgImage} bgSize="100%" minHeight="100vh">
      <NavBar></NavBar>
      <HStack gap={0} alignItems="top">
        <BodyContainer>
          <Outlet />
          {children}
        </BodyContainer>
      </HStack>
    </Box>
  );
};

export default Layout;
