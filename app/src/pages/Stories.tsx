import { Button, useDisclosure } from "@chakra-ui/react";
import PageHeader from "../components/PageHeader";
import { StoryFormModal, StoryGrid, StoryQuery, useStories } from "../stories";
import { useAuth } from "../users";
import { useContext } from "react";
import PageContext, { PageContextType } from "./pageContext";

const Stories = () => {
  const {
    isOpen: newIsOpen,
    onOpen: newOnOpen,
    onClose: newOnClose,
  } = useDisclosure();
  const pageContext = useContext(PageContext);
  const { signedIn } = useAuth();
  const storyQuery: StoryQuery =
    pageContext === PageContextType.public ? { is_published: true } : {};
  const storiesDisabled = pageContext !== PageContextType.public && !signedIn;
  const {
    data: stories,
    error,
    isLoading,
  } = useStories(storyQuery, storiesDisabled);

  if (isLoading) return null;
  if (error) throw error;

  return (
    <>
      {pageContext === PageContextType.design && signedIn && (
        <PageHeader
          rightButton={
            <Button
              size="md"
              bgColor="brand.bg"
              color="inherit"
              onClick={newOnOpen}
            >
              Add story
            </Button>
          }
        >
          All stories
        </PageHeader>
      )}
      {stories && (
        <>
          <StoryGrid stories={stories} />
          {pageContext === PageContextType.design && (
            <StoryFormModal
              title="Add Story"
              isOpen={newIsOpen}
              onClose={newOnClose}
            />
          )}
        </>
      )}
    </>
  );
};

export default Stories;
