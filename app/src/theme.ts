import { extendTheme, type ThemeConfig } from "@chakra-ui/react";

const config: ThemeConfig = {
  initialColorMode: "light",
  useSystemColorMode: false,
};

const theme = extendTheme({
  config,
  styles: {
    global: {
      body: { fontFamily: "Papyrus, fantasy", textColor: "brand.100" },
    },
  },
  colors: {
    brand: {
      100: "rgb(30, 44, 25)",
      200: "rgb(237, 254, 255)",
      300: "rgb(82, 102, 67)",
    },
  },
});

export default theme;
