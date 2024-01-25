import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import APIClient from "./api-client";
import { AxiosRequestConfig } from "axios";

export interface AddDataContext<S> {
  prevData: S[];
}

export interface UpdateDataContext<S> {
  prevDataList?: S[];
  prevData?: S;
}

export interface DeleteDataContext<S> {
  prevData: S[];
}

interface A {
  id: number;
}

export interface AddArgs<S, Q = S> {
  onAdd?: () => void;
  onSuccess?: (newData: S) => void;
  queryMutation?: (newData: Q, dataList: S[]) => S[];
}

export interface UpdateArgs<S> {
  onUpdate?: () => void;
  onSuccess?: () => void;
  queryMutation?: (newData: S, dataList: S[]) => S[];
  endpointIgnoresId?: boolean;
}

export interface DeleteArgs<S> {
  onDelete?: () => void;
  onSuccess?: () => void;
  queryMutation?: (dataId: number, dataList: S[]) => S[];
}

export interface EnrollArgs {
  onEnroll?: () => void;
  onSuccess?: () => void;
  onError?: () => void;
}

// Typical API hooks (S: response body; Q: request body)
export default class APIHooks<S extends A, Q = S> {
  client: APIClient<S, Q>;
  cacheKey: (string | number)[];
  staleTime: number;

  constructor(client: APIClient<S, Q>, cacheKey: string[], staleTime: number) {
    this.client = client;
    this.cacheKey = cacheKey;
    this.staleTime = staleTime;
  }

  useData = (id?: number, disabled?: boolean) => {
    const singleCacheKey = [...this.cacheKey];
    if (id) singleCacheKey.push(id);
    return useQuery<S, Error>({
      queryKey: singleCacheKey,
      queryFn: () => this.client.get(id),
      staleTime: this.staleTime,
      enabled: !disabled,
    });
  };

  useDataList = (config?: AxiosRequestConfig, disabled?: boolean) =>
    useQuery<S[], Error>({
      queryKey: config ? [...this.cacheKey, config] : this.cacheKey,
      queryFn: () => this.client.getAll(config),
      staleTime: this.staleTime,
      enabled: !disabled,
    });

  useAdd = (addArgs?: AddArgs<S, Q>) => {
    const queryClient = useQueryClient();
    const { onAdd, onSuccess, queryMutation } = addArgs || {};

    const addData = useMutation<S, Error, Q, AddDataContext<S>>({
      mutationFn: (data: Q) => this.client.post(data),
      onMutate: (newData: Q) => {
        const prevData = queryClient.getQueryData<S[]>(this.cacheKey) || [];
        queryClient.setQueryData<S[]>(this.cacheKey, (dataList = []) => {
          if (queryMutation) {
            return queryMutation(newData, dataList);
          } else {
            return [...dataList, { id: 0, ...newData } as unknown as S];
          }
        });
        if (onAdd) onAdd();
        return { prevData };
      },
      onSuccess: (newData, submittedData) => {
        queryClient.setQueryData<S[]>(this.cacheKey, (dataList) =>
          dataList?.map((data) => (data.id === 0 ? newData : data))
        );
        if (onSuccess) onSuccess(newData);
        if (!submittedData) return; // this is silly, but npm run build is complaining about not using newData
      },
      onError: (error, newData, context) => {
        if (!error || !context) return;
        queryClient.setQueryData<S[]>(this.cacheKey, () => context.prevData);
        if (!newData) return; // this is silly, but npm run build is complaining about not using newData
      },
    });

    return addData;
  };

  useUpdate = (updateArgs?: UpdateArgs<S>) => {
    const { onUpdate, onSuccess, queryMutation, endpointIgnoresId } =
      updateArgs || {};
    const queryClient = useQueryClient();

    const udpateData = useMutation<S, Error, S, UpdateDataContext<S>>({
      mutationFn: (data: S) =>
        this.client.put(endpointIgnoresId ? undefined : data.id, {
          ...data,
        } as unknown as Q),
      onMutate: (newData: S) => {
        // Update in list
        let prevDataList = undefined;
        if (!endpointIgnoresId) {
          prevDataList = queryClient.getQueryData<S[]>(this.cacheKey) || [];
          queryClient.setQueryData<S[]>(this.cacheKey, (dataList = []) => {
            if (queryMutation) {
              return queryMutation(newData, dataList);
            } else {
              return dataList.map((data) =>
                data.id === newData.id ? newData : data
              );
            }
          });
        }

        // Also update individual data cache
        const singleCacheKey = [...this.cacheKey];
        if (!endpointIgnoresId) singleCacheKey.push(newData.id);
        const prevData = queryClient.getQueryData<S[]>(singleCacheKey);
        if (prevData) queryClient.setQueryData<S>(singleCacheKey, newData);

        if (onUpdate) onUpdate();
        return { prevDataList, prevData } as UpdateDataContext<S>;
      },
      onSuccess: onSuccess,
      onError: (error, newData, context) => {
        if (!error || !context) return;

        if (context.prevDataList) {
          queryClient.setQueryData<S[]>(
            this.cacheKey,
            () => context.prevDataList
          );
        }

        if (context.prevData) {
          const singleCacheKey = [...this.cacheKey];
          singleCacheKey.push(context.prevData.id);
          queryClient.setQueryData<S>(singleCacheKey, () => context.prevData);
        }
        if (!newData) return; // this is silly, but npm run build is complaining about not using newData
      },
    });

    return udpateData;
  };

  useDelete = (deleteArgs?: DeleteArgs<S>) => {
    const queryClient = useQueryClient();
    const { onDelete, onSuccess, queryMutation } = deleteArgs || {};

    const deleteData = useMutation<any, Error, number, DeleteDataContext<S>>({
      mutationFn: (dataId: number) => this.client.delete(dataId),
      onMutate: (dataId: number) => {
        const prevData = queryClient.getQueryData<S[]>(this.cacheKey) || [];
        queryClient.setQueryData<S[]>(this.cacheKey, (dataList = []) => {
          if (queryMutation) {
            return queryMutation(dataId, dataList);
          } else {
            return dataList.filter((data) => data.id !== dataId);
          }
        });
        if (onDelete) onDelete();
        return { prevData };
      },
      onSuccess: onSuccess,
      onError: (error, newData, context) => {
        if (!error || !context) return;
        queryClient.setQueryData<S[]>(this.cacheKey, () => context.prevData);
        if (!newData) return; // this is silly, but npm run build is complaining about not using newData
      },
    });

    return deleteData;
  };

  // "Enroll" uses post to add one existing object to another
  // E.g. a student to a camp: neiher is created as an object, but the student is added to the camp
  useEnroll = (enrollArgs?: EnrollArgs) => {
    const queryClient = useQueryClient();
    const { onEnroll, onSuccess, onError } = enrollArgs || {};

    const enrollData = useMutation<S, Error, number>({
      mutationFn: (dataId: number) => this.client.post(dataId),
      onMutate: () => {
        if (onEnroll) onEnroll();
      },
      onError: onError,
      onSuccess: () => {
        queryClient.invalidateQueries({ queryKey: this.cacheKey });
        if (onSuccess) onSuccess();
      },
    });

    return enrollData;
  };
}
