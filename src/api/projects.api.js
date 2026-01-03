import api from "./axios";

export const fetchProjects = async () => {
  const response = await api.get("projects/");
  return response.data;
};
