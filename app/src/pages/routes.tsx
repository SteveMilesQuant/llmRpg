import { createBrowserRouter } from "react-router-dom";
import Layout from "./Layout";
import ErrorPage from "./ErrorPage";
import Home from "./Home";
import PrivateRoutes from "./PrivateRoutes";
import Stories from "./Stories";
import PageContext, { PageContextType } from "./pageContext";
import Design from "./Design";
import Adventure from "./Adventure";

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
        element: (
          <PageContext.Provider value={PageContextType.public}>
            <Layout />
          </PageContext.Provider>
        ),
        children: [
          { index: true, element: <Home /> },
          {
            path: "adventure",
            element: <Adventure />,
          },
        ],
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
                element: <Design />,
              },
            ],
          },
        ],
      },
    ],
  },
]);

export default router;
