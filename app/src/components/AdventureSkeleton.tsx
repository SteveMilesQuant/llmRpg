import { Card, CardBody, SkeletonText } from "@chakra-ui/react";

const AdventureSkeleton = () => {
  const cardRepeater = [1, 2, 3, 4];
  return (
    <>
      <Card opacity="0.8">
        <CardBody bgColor="brand.200" opacity="0.9" borderRadius={15}>
          <SkeletonText height="100px" />
        </CardBody>
      </Card>
      {cardRepeater.map((i) => (
        <Card opacity="0.8" key={i}>
          <CardBody bgColor="white" opacity="0.9" borderRadius={15}>
            <SkeletonText />
          </CardBody>
        </Card>
      ))}
    </>
  );
};

export default AdventureSkeleton;
