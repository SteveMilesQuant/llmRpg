import { Tabs, TabList, Tab, TabPanels, TabPanel } from "@chakra-ui/react";
import { Story } from "../Story";
import StoryForm from "./StoryForm";
import { Locations } from "../../locations";
import { Characters } from "../../characters";

interface Props {
  story: Story;
}

const StoryTabs = ({ story }: Props) => {
  return (
    <Tabs variant="enclosed">
      <TabList color="brand.100">
        <Tab bgColor="white" marginRight={0.5}>
          Story
        </Tab>
        <Tab bgColor="white" marginRight={0.5}>
          Locations
        </Tab>
        <Tab bgColor="white" marginRight={0.5}>
          Characters
        </Tab>
      </TabList>
      <TabPanels>
        <TabPanel bgColor="white">
          <StoryForm story={story} />
        </TabPanel>
        <TabPanel bgColor="white">
          <Locations storyId={story.id} />
        </TabPanel>
        <TabPanel bgColor="white">
          <Characters storyId={story.id} />
        </TabPanel>
      </TabPanels>
    </Tabs>
  );
};

export default StoryTabs;
