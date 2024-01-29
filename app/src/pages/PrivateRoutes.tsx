import { Navigate, Outlet } from "react-router-dom";
import { useAuth } from "../users";

const PrivateRoutes = () => {
  const { signedIn, isChecking } = useAuth();
  if (!signedIn && !isChecking) return <Navigate to="/design" />;
  return <Outlet />;
};

export default PrivateRoutes;
