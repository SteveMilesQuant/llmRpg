import ms from "ms";
import APIClient from "../../services/api-client";
import APIHooks, {
  AddArgs,
  AddDataContext,
  DeleteArgs,
  DeleteDataContext,
  UpdateArgs,
  UpdateDataContext,
} from "../../services/api-hooks";
import { CACHE_KEY_LOCATIONS, Location, LocationData } from "../Location";
import { CACHE_KEY_STORIES } from "../../stories";
import { UseMutationResult, UseQueryResult } from "@tanstack/react-query";

const useLocationHooks = (storyId: number) =>
  new APIHooks<Location, LocationData>(
    new APIClient<Location, LocationData>(`/stories/${storyId}/locations`),
    [...CACHE_KEY_STORIES, storyId.toString(), ...CACHE_KEY_LOCATIONS],
    ms("5m")
  );

const useStoryLocations = (storyId?: number) => {
  if (!storyId) return {} as UseQueryResult<Location[], Error>;
  const locationHooks = useLocationHooks(storyId);
  return locationHooks.useDataList();
};
export default useStoryLocations;

export const useAddLocation = (
  storyId?: number,
  options?: AddArgs<Location, LocationData>
) => {
  if (!storyId)
    return {} as UseMutationResult<
      Location,
      Error,
      LocationData,
      AddDataContext<Location>
    >;
  const locationHooks = useLocationHooks(storyId);
  return locationHooks.useAdd(options);
};

export const useUpdateLocation = (
  storyId?: number,
  options?: UpdateArgs<Location>
) => {
  if (!storyId)
    return {} as UseMutationResult<
      Location,
      Error,
      Location,
      UpdateDataContext<Location>
    >;
  const locationHooks = useLocationHooks(storyId);
  return locationHooks.useUpdate(options);
};

export const useDeleteLocation = (
  storyId?: number,
  options?: DeleteArgs<Location>
) => {
  if (!storyId)
    return {} as UseMutationResult<
      any,
      Error,
      number,
      DeleteDataContext<Location>
    >;
  const locationHooks = useLocationHooks(storyId);
  return locationHooks.useDelete(options);
};

export const useLocation = (storyId?: number, locationId?: number) => {
  if (!storyId || !locationId) return {} as UseQueryResult<Location, Error>;
  const locationHooks = useLocationHooks(storyId);
  return locationHooks.useData(locationId);
};
