import { useEffect } from "react";
import { useParams } from "react-router-dom";
import useSession from "../hooks/useSession";
import useStoryQuery from "../hooks/useStoryQuery";

const Story = () => {
  const { id: idStr } = useParams();
  const id = idStr ? parseInt(idStr) : undefined;
  const { onStart } = useSession();
  const { narratorResponse } = useStoryQuery();

  useEffect(() => {
    if (id) onStart(id);
  }, []);

  return <div>{narratorResponse}</div>;
};

export default Story;
