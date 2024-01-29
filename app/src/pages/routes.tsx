import { createBrowserRouter } from "react-router-dom";
import Layout from "./Layout";
import ErrorPage from "./ErrorPage";
import Home from "./Home";
import PrivateRoutes from "./PrivateRoutes";
import Stories from "./Stories";
import Story from "./Story";
import PageContext, { PageContextType } from "./pageContext";

const router = createBrowserRouter([
  {
    path: "/",
    errorElement: (
      <PageContext.Provider value={PageContextType.public}>
        <Layout>
          <ErrorPage />
        </Layout>
      </PageContext.Provider>
    ),
    children: [
      {
        index: true,
        element: (
          <PageContext.Provider value={PageContextType.public}>
            <Layout>
              <Home />
            </Layout>
          </PageContext.Provider>
        ),
      },
      {
        path: "design",
        element: (
          <PageContext.Provider value={PageContextType.design}>
            <Layout />
          </PageContext.Provider>
        ),
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
