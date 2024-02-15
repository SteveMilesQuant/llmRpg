import { Box, Image } from "@chakra-ui/react";
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
  if (isLoading || !baseImage) return null;

  return (
    <Box marginX="auto">
      <Image
        src={baseImage.url}
        alt={"AI generated image of the current character"}
        width="240px"
        height="240px"
      />
    </Box>
  );
};

export default CharacterImage;
