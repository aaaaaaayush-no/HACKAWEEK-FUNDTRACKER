import api from "./axios";

export const submitProgress = async (projectId, data) => {
  const formData = new FormData();
  formData.append("physical_progress", data.physical_progress);
  formData.append("financial_progress", data.financial_progress);
  formData.append("project", projectId);

  if (data.images) {
    for (let i = 0; i < data.images.length; i++) {
      formData.append("images", data.images[i]);
    }
  }

  return api.post(`progress/`, formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });
};

export const getPendingProgress = async () => {
  const response = await api.get('/progress/pending/');
  return response.data;
};

export const approveProgress = async (id) => {
  const response = await api.post(`/progress/${id}/approve/`);
  return response.data;
};

export const rejectProgress = async (id) => {
  const response = await api.post(`/progress/${id}/reject/`);
  return response.data;
};
