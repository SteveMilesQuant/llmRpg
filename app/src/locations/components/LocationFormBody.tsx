import {
  FormControl,
  FormLabel,
  Input,
  Select,
  SimpleGrid,
  Textarea,
} from "@chakra-ui/react";
import { FieldErrors, UseFormRegister } from "react-hook-form";
import { FormData } from "../hooks/useLocationForm";
import InputError from "../../components/InputError";
import { useCharacters } from "../../characters";

interface Props {
  register: UseFormRegister<FormData>;
  errors: FieldErrors<FormData>;
  isReadOnly?: boolean;
  showStartingCharacter?: boolean;
  storyId?: number;
}

const LocationFormBody = ({
  register,
  errors,
  isReadOnly,
  showStartingCharacter,
  storyId,
}: Props) => {
  const { data: characters } = useCharacters(storyId);

  return (
    <SimpleGrid columns={1} gap={5}>
      <FormControl>
        <FormLabel textColor="white">Name</FormLabel>
        <InputError
          label={errors.name?.message}
          isOpen={errors.name ? true : false}
        >
          <Input
            bgColor="brand.bg"
            {...register("name")}
            type="text"
            isReadOnly={isReadOnly}
          />
        </InputError>
      </FormControl>
      {showStartingCharacter && (
        <FormControl>
          <FormLabel textColor="white">Starting character</FormLabel>
          <InputError
            label={errors.starting_character_id?.message}
            isOpen={errors.starting_character_id ? true : false}
          >
            <Select
              {...register("starting_character_id")}
              disabled={isReadOnly}
              bgColor="brand.bg"
            >
              <option value="">Select character</option>{" "}
              {characters?.map((character) => (
                <option key={character.id} value={character.id}>
                  {character.name}
                </option>
              ))}
            </Select>
          </InputError>
        </FormControl>
      )}
      <FormControl>
        <FormLabel textColor="white">Description</FormLabel>
        <InputError
          label={errors.description?.message}
          isOpen={errors.description ? true : false}
        >
          <Input
            {...register("description")}
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

export default LocationFormBody;
