import {
  FormControl,
  FormLabel,
  Input,
  Select,
  Stack,
  Textarea,
} from "@chakra-ui/react";
import {
  FieldErrors,
  UseFormGetValues,
  UseFormRegister,
} from "react-hook-form";
import { FormData } from "../hooks/useStoryForm";
import InputError from "../../components/InputError";
import { useLocations } from "../../locations";

interface Props {
  register: UseFormRegister<FormData>;
  errors: FieldErrors<FormData>;
  getValues: UseFormGetValues<FormData>;
  isReadOnly?: boolean;
  showLocation?: boolean;
  storyId?: number;
}

const StoryFormBody = ({
  register,
  errors,
  getValues,
  isReadOnly,
  showLocation,
  storyId,
}: Props) => {
  const { data: locations } = useLocations(storyId);

  return (
    <Stack spacing={5}>
      <FormControl>
        <FormLabel>Title</FormLabel>
        <InputError
          label={errors.title?.message}
          isOpen={errors.title ? true : false}
        >
          <Input {...register("title")} type="text" isReadOnly={isReadOnly} />
        </InputError>
      </FormControl>
      <FormControl>
        <FormLabel>Blurb</FormLabel>
        <InputError
          label={errors.blurb?.message}
          isOpen={errors.blurb ? true : false}
        >
          <Input
            {...register("blurb")}
            as={Textarea}
            size="xl"
            height="7rem"
            isReadOnly={isReadOnly}
          />
        </InputError>
      </FormControl>
      {showLocation && (
        <FormControl>
          <FormLabel>Starting location</FormLabel>
          <InputError
            label={errors.starting_location_id?.message}
            isOpen={errors.starting_location_id ? true : false}
          >
            <Select
              {...register("starting_location_id")}
              disabled={isReadOnly}
              value={isReadOnly ? getValues("starting_location_id") : undefined}
            >
              <option value="">Select location</option>
              {locations?.map((location) => (
                <option key={location.id} value={location.id}>
                  {location.name}
                </option>
              ))}
            </Select>
          </InputError>
        </FormControl>
      )}
      <FormControl>
        <FormLabel>Setting</FormLabel>
        <InputError
          label={errors.setting?.message}
          isOpen={errors.setting ? true : false}
        >
          <Input
            {...register("setting")}
            as={Textarea}
            size="xl"
            height="15rem"
            isReadOnly={isReadOnly}
          />
        </InputError>
      </FormControl>
    </Stack>
  );
};

export default StoryFormBody;
