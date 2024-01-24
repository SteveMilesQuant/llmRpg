import { createBrowserRouter } from "react-router-dom";
import Layout from "./Layout";
import ErrorPage from "./ErrorPage";
import Home from "./Home";
import PrivateRoutes from "./PrivateRoutes";
import Stories from "./Stories";
import AdminLayout from "./AdminLayout";
import Story from "./Story";

const router = createBrowserRouter([
  {
    path: "/",
    errorElement: (
      <Layout>
        <ErrorPage />
      </Layout>
    ),
    children: [
      {
        index: true,
        element: (
          <Layout>
            <Home />
          </Layout>
        ),
      },
      {
        path: "stories",
        element: <AdminLayout />,
        children: [
          { index: true, element: <Stories /> },
          {
            element: <PrivateRoutes />,
            children: [
              {
                path: ":id",
                element: <Story />,
              },
            ],
          },
        ],
      },
    ],
  },
]);

export default router;
