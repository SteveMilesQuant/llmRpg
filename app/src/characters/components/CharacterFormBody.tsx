import {
  FormControl,
  FormLabel,
  Input,
  SimpleGrid,
  Textarea,
} from "@chakra-ui/react";
import { FieldErrors, UseFormRegister } from "react-hook-form";
import { FormData } from "../hooks/useCharacterForm";
import InputError from "../../components/InputError";

interface Props {
  register: UseFormRegister<FormData>;
  errors: FieldErrors<FormData>;
  isReadOnly?: boolean;
}

const CharacterFormBody = ({ register, errors, isReadOnly }: Props) => {
  return (
    <SimpleGrid columns={1} gap={5}>
      <FormControl>
        <FormLabel>Name</FormLabel>
        <InputError
          label={errors.name?.message}
          isOpen={errors.name ? true : false}
        >
          <Input {...register("name")} type="text" isReadOnly={isReadOnly} />
        </InputError>
      </FormControl>
      <FormControl>
        <FormLabel>Description</FormLabel>
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
          />
        </InputError>
      </FormControl>
    </SimpleGrid>
  );
};

export default CharacterFormBody;
