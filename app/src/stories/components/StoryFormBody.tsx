import {
  FormControl,
  FormLabel,
  Input,
  Stack,
  Textarea,
} from "@chakra-ui/react";
import { FieldErrors, UseFormRegister } from "react-hook-form";
import { FormData } from "../hooks/useStoryForm";
import InputError from "../../components/InputError";

interface Props {
  register: UseFormRegister<FormData>;
  errors: FieldErrors<FormData>;
  isReadOnly?: boolean;
}

const StoryFormBody = ({ register, errors, isReadOnly }: Props) => {
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
