import { useParams } from "react-router-dom";
import PageHeader from "../components/PageHeader";
import {
  CACHE_KEY_STORIES,
  StoryTabs,
  useStory,
  useUpdateStory,
} from "../stories";
import { Button } from "@chakra-ui/react";
import { useQueryClient } from "@tanstack/react-query";

const Design = () => {
  const { id: idStr } = useParams();
  const id = idStr ? parseInt(idStr) : undefined;

  const { data: story, error, isLoading } = useStory(id);

  const queryClient = useQueryClient();
  const updateStory = useUpdateStory({
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: CACHE_KEY_STORIES });
      queryClient.invalidateQueries({
        queryKey: [...CACHE_KEY_STORIES, story?.id.toString()],
      });
    },
  });

  if (isLoading || !story) return null;
  if (error) throw error;

  return (
    <>
      <PageHeader
        hideUnderline={true}
        rightButton={
          <Button
            size="md"
            variant="outline"
            color="inherit"
            onClick={() => {
              updateStory.mutate({
                ...story,
                is_published: !story.is_published,
              });
            }}
          >
            {story.is_published ? "Unpublish" : "Publish"}
          </Button>
        }
      >
        {story?.title}
      </PageHeader>
      <StoryTabs story={story} />
    </>
  );
};

export default Design;
