import { Outlet } from "react-router-dom";
import { HStack } from "@chakra-ui/react";
import AdminNavBar from "../components/AdminNavBar";
import { ReactNode } from "react";
import BodyContainer from "../components/BodyContainer";

interface Props {
  children?: ReactNode;
}

const AdminLayout = ({ children }: Props) => {
  // Include both Outlet and children, to allow both contexts

  return (
    <>
      <AdminNavBar></AdminNavBar>
      <HStack gap={0} alignItems="top">
        <BodyContainer>
          <Outlet />
          {children}
        </BodyContainer>
      </HStack>
    </>
  );
};

export default AdminLayout;
