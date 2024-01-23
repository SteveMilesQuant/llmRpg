import axios, { AxiosRequestConfig, AxiosResponse } from "axios";

// Create axios instance
export const axiosInstance = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
});

// Create client (S: response body; Q: request body)
class APIClient<S, Q = S> {
  endpoint: string;

  constructor(endpoint: string) {
    this.endpoint = endpoint;
  }

  getAll = (config?: AxiosRequestConfig) => {
    return axiosInstance
      .get<S[]>(this.endpoint, config)
      .then((res) => res.data);
  };

  get = (id?: number) => {
    return axiosInstance
      .get<S>(id ? this.endpoint + "/" + id : this.endpoint)
      .then((res) => res.data);
  };

  post = (data: Q | number | string) => {
    if (typeof data === "number" || typeof data === "string") {
      // This isn't the best way to do this - maybe come back to it later
      // instanceof doesn't work with generic types
      return axiosInstance
        .post<null, AxiosResponse<S>>(this.endpoint + `/${data}`)
        .then((res) => res.data);
    } else {
      return axiosInstance
        .post<Q, AxiosResponse<S>>(this.endpoint, data)
        .then((res) => res.data);
    }
  };

  put = (id?: number, data?: Q) => {
    return axiosInstance
      .put<Q, AxiosResponse<S>>(
        id ? this.endpoint + "/" + id : this.endpoint,
        data
      )
      .then((res) => res.data);
  };

  delete = (id: number | string) => {
    return axiosInstance.delete(this.endpoint + "/" + id);
  };
}

export default APIClient;
