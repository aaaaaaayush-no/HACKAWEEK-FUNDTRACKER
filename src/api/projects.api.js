import api from "./axios";

export const getProjects = async () => {
  const response = await api.get("projects/");
  return response.data;
};

export const getProjectById = async (id) => {
  const response = await api.get(`projects/${id}/`);
  return response.data;
};

// Deprecated: Use getProjects instead
export const fetchProjects = getProjects;
