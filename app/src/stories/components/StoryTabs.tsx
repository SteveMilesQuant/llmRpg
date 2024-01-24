import { Tabs, TabList, Tab, TabPanels, TabPanel } from "@chakra-ui/react";
import { Story } from "../Story";
import StoryForm from "./StoryForm";
import { Locations } from "../../locations";

interface Props {
  story: Story;
}

const StoryTabs = ({ story }: Props) => {
  return (
    <Tabs variant="enclosed">
      <TabList>
        <Tab>Story</Tab>
        <Tab>Locations</Tab>
        <Tab>Characters</Tab>
      </TabList>
      <TabPanels>
        <TabPanel>
          <StoryForm story={story} />
        </TabPanel>
        <TabPanel>
          <Locations storyId={story.id} />
        </TabPanel>
        <TabPanel></TabPanel>
      </TabPanels>
    </Tabs>
  );
};

export default StoryTabs;
