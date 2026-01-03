import api from "./axios";

// Material APIs
export const getMaterials = async (projectId = null) => {
  const params = projectId ? { project: projectId } : {};
  const response = await api.get("materials/", { params });
  return response.data;
};

export const getMaterialById = async (id) => {
  const response = await api.get(`materials/${id}/`);
  return response.data;
};

export const createMaterial = async (data) => {
  const response = await api.post("materials/", data);
  return response.data;
};

export const verifyMaterial = async (id) => {
  const response = await api.post(`materials/${id}/verify/`);
  return response.data;
};

// Material Payment APIs
export const getMaterialPayments = async () => {
  const response = await api.get("material-payments/");
  return response.data;
};

export const createMaterialPayment = async (data) => {
  const response = await api.post("material-payments/", data);
  return response.data;
};

// Get project materials via project endpoint
export const getProjectMaterials = async (projectId) => {
  const response = await api.get(`projects/${projectId}/materials/`);
  return response.data;
};
