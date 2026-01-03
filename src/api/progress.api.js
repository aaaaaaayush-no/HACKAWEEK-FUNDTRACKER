import api from "./axios";

export const submitProgress = async (projectId, data) => {
  const formData = new FormData();
  formData.append("physical_progress", data.physical_progress);
  formData.append("financial_progress", data.financial_progress);

  if (data.images) {
    for (let i = 0; i < data.images.length; i++) {
      formData.append("images", data.images[i]);
    }
  }

  return api.post(`projects/${projectId}/progress/`, formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });
};
