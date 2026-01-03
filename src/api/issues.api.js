import api from "./axios";

// Issue Report APIs
export const getIssues = async () => {
  const response = await api.get("issues/");
  return response.data;
};

export const getIssueById = async (id) => {
  const response = await api.get(`issues/${id}/`);
  return response.data;
};

export const createIssue = async (data) => {
  const response = await api.post("issues/", data);
  return response.data;
};

export const verifyIssue = async (id) => {
  const response = await api.post(`issues/${id}/verify/`);
  return response.data;
};

export const forgiveIssue = async (id, reason) => {
  const response = await api.post(`issues/${id}/forgive/`, { reason });
  return response.data;
};

export const penalizeIssue = async (id) => {
  const response = await api.post(`issues/${id}/penalize/`);
  return response.data;
};

// Get project issues via project endpoint
export const getProjectIssues = async (projectId) => {
  const response = await api.get(`projects/${projectId}/issues/`);
  return response.data;
};

// Issue Evidence APIs
export const uploadIssueEvidence = async (issueId, formData) => {
  formData.append("issue", issueId);
  const response = await api.post("issue-evidence/", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return response.data;
};
