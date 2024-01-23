import APIClient from "../../services/api-client";
import { User, UserData } from "../User";
import APIHooks, { UpdateArgs } from "../../services/api-hooks";
import ms from "ms";
import useAuth from "./useAuth";

export const CACHE_KEY_USER = ["user"];

const userHooks = new APIHooks<User, UserData>(
  new APIClient<User, UserData>("/user"),
  CACHE_KEY_USER,
  ms("5m")
);

export const useUpdateUser = (updateArgs?: UpdateArgs<User>) =>
  userHooks.useUpdate({ ...updateArgs, endpointIgnoresId: true });

const useUser = () => {
  const { signedIn } = useAuth();
  return userHooks.useData(undefined, !signedIn);
};

export default useUser;
