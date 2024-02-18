import { Box, Image, Spinner } from "@chakra-ui/react";
import { useCharacterBaseImage } from "../hooks/useCharacters";

interface Props {
  storyId: number;
  characterId: number;
}

const CharacterImage = ({ storyId, characterId }: Props) => {
  const {
    data: baseImage,
    isLoading,
    error,
  } = useCharacterBaseImage(storyId, characterId);

  if (error) throw error;
  if (isLoading)
    return (
      <Box
        marginX="auto"
        borderRadius={15}
        paddingTop={4}
        paddingRight={5}
        paddingBottom={5}
        paddingLeft={4}
        bgColor="rgba(255,255,255,0.8)"
      >
        <Box width="240px" height="240px">
          <Box width="fit-content" margin="auto">
            <Spinner size="xl" />
          </Box>
        </Box>
      </Box>
    );
  if (!baseImage) return null;

  return (
    <Box
      marginX="auto"
      borderRadius={15}
      paddingTop={4}
      paddingRight={5}
      paddingBottom={5}
      paddingLeft={4}
      bgColor="rgba(255,255,255,0.8)"
    >
      <Image
        src={baseImage.url}
        alt={"AI generated image of the current character"}
        width="240px"
        height="240px"
        borderRadius={15}
        boxShadow="10px 10px 10px rgba(0, 0, 0, 0.8)"
      />
    </Box>
  );
};

export default CharacterImage;
