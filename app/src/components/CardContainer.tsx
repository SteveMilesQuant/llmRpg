import { Card, CardBody, LinkBox } from "@chakra-ui/react";
import { ReactNode } from "react";

interface Props {
  children: ReactNode;
}

const CardContainer = ({ children }: Props) => {
  return (
    <LinkBox
      as={Card}
      _hover={{
        bgColor: "gray.200",
        transform: "scale(1.03)",
        transition: "transform .2s ease-in",
      }}
    >
      <CardBody textColor="brand.100">{children}</CardBody>
    </LinkBox>
  );
};

export default CardContainer;
