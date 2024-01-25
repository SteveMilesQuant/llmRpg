import { Button, useDisclosure } from "@chakra-ui/react";
import PageHeader from "../components/PageHeader";
import { StoryFormModal, StoryGrid, useStories } from "../stories";
import { useAuth } from "../users";

const Stories = () => {
  const {
    isOpen: newIsOpen,
    onOpen: newOnOpen,
    onClose: newOnClose,
  } = useDisclosure();

  const { signedIn } = useAuth();
  const { data: stories, error, isLoading } = useStories(!signedIn);

  if (isLoading || !signedIn) return null;
  if (error) throw error;

  return (
    <>
      <PageHeader
        rightButton={
          signedIn && (
            <Button
              size="md"
              variant="outline"
              color="inherit"
              onClick={newOnOpen}
            >
              Add story
            </Button>
          )
        }
      >
        All stories
      </PageHeader>
      {stories && (
        <>
          <StoryGrid stories={stories} />
          <StoryFormModal
            title="Add Story"
            isOpen={newIsOpen}
            onClose={newOnClose}
          />
        </>
      )}
    </>
  );
};

export default Stories;
