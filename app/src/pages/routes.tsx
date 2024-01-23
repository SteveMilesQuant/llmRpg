import { createBrowserRouter } from "react-router-dom";
import Layout from "./Layout";
import ErrorPage from "./ErrorPage";
import Home from "./Home";
import PrivateRoutes from "./PrivateRoutes";
import Admin from "./Admin";
import AdminLayout from "./AdminLayout";

const router = createBrowserRouter([
  {
    path: "/",
    children: [
      {
        index: true,
        element: (
          <Layout>
            <Home />
          </Layout>
        ),
        errorElement: (
          <Layout>
            <ErrorPage />
          </Layout>
        ),
      },
      {
        path: "admin",
        element: <AdminLayout />,
        children: [
          { index: true, element: <Admin /> },
          {
            element: <PrivateRoutes />,
            children: [],
          },
        ],
      },
    ],
  },
]);

export default router;
