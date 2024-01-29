import { createContext } from "react";

export enum PageContextType {
  public,
  design,
}

const PageContext = createContext<PageContextType>(PageContextType.public);

export default PageContext;
