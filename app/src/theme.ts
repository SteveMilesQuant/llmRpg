import { extendTheme, type ThemeConfig } from "@chakra-ui/react";

const config: ThemeConfig = {
  initialColorMode: "light",
  useSystemColorMode: false,
};

const theme = extendTheme({
  config,
  styles: {
    global: { body: { fontFamily: "Georgia", textColor: "brand.100" } },
  },
  colors: {
    brand: {
      100: "rgb(4,0,154)",
      200: "rgb(192,254,252)",
      300: "rgb(119,172,241)",
    },
  },
});

export default theme;
