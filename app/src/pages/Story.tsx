import { useEffect } from "react";
import { useParams } from "react-router-dom";
import { useSession } from "../users";

const Story = () => {
  const { id: idStr } = useParams();
  const id = idStr ? parseInt(idStr) : undefined;
  const { onStart } = useSession();

  useEffect(() => {
    if (id) onStart(id);
  }, []);

  return <div>Story</div>;
};

export default Story;
