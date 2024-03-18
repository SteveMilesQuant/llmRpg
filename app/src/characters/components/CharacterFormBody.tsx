import {
  FormControl,
  FormLabel,
  Input,
  Select,
  SimpleGrid,
  Textarea,
} from "@chakra-ui/react";
import { FieldErrors, UseFormRegister } from "react-hook-form";
import { FormData } from "../hooks/useCharacterForm";
import InputError from "../../components/InputError";
import { useLocations } from "../../locations";

interface Props {
  register: UseFormRegister<FormData>;
  errors: FieldErrors<FormData>;
  isReadOnly?: boolean;
  showLocation?: boolean;
  storyId?: number;
}

const CharacterFormBody = ({
  register,
  errors,
  isReadOnly,
  showLocation,
  storyId,
}: Props) => {
  const { data: locations } = useLocations(storyId);

  return (
    <SimpleGrid columns={1} gap={5}>
      <FormControl>
        <FormLabel textColor="white">Name</FormLabel>
        <InputError
          label={errors.name?.message}
          isOpen={errors.name ? true : false}
        >
          <Input
            {...register("name")}
            type="text"
            isReadOnly={isReadOnly}
            bgColor="brand.bg"
          />
        </InputError>
      </FormControl>
      {showLocation && (
        <FormControl>
          <FormLabel textColor="white">Location</FormLabel>
          <InputError
            label={errors.location_id?.message}
            isOpen={errors.location_id ? true : false}
          >
            <Select
              {...register("location_id")}
              disabled={isReadOnly}
              bgColor="brand.bg"
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
        <FormLabel textColor="white">Public Description</FormLabel>
        <InputError
          label={errors.public_description?.message}
          isOpen={errors.public_description ? true : false}
        >
          <Input
            {...register("public_description")}
            as={Textarea}
            size="xl"
            height="5rem"
            isReadOnly={isReadOnly}
            bgColor="brand.bg"
          />
        </InputError>
      </FormControl>
      <FormControl>
        <FormLabel textColor="white">Private Description</FormLabel>
        <InputError
          label={errors.private_description?.message}
          isOpen={errors.private_description ? true : false}
        >
          <Input
            {...register("private_description")}
            as={Textarea}
            size="xl"
            height="15rem"
            isReadOnly={isReadOnly}
            bgColor="brand.bg"
          />
        </InputError>
      </FormControl>
    </SimpleGrid>
  );
};

export default CharacterFormBody;
