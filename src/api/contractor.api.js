import api from "./axios";

// Contractor Profile APIs
export const getContractorProfiles = async () => {
  const response = await api.get("contractor-profiles/");
  return response.data;
};

export const getContractorProfile = async (id) => {
  const response = await api.get(`contractor-profiles/${id}/`);
  return response.data;
};

export const checkContractorEligibility = async (id) => {
  const response = await api.get(`contractor-profiles/${id}/check_eligibility/`);
  return response.data;
};

export const getSuspendedContractors = async () => {
  const response = await api.get("contractor-profiles/suspended/");
  return response.data;
};

// Contractor Certificate APIs
export const getContractorCertificates = async () => {
  const response = await api.get("contractor-certificates/");
  return response.data;
};

export const createContractorCertificate = async (data) => {
  const response = await api.post("contractor-certificates/", data);
  return response.data;
};

// Contractor Skill APIs
export const getContractorSkills = async () => {
  const response = await api.get("contractor-skills/");
  return response.data;
};

export const createContractorSkill = async (data) => {
  const response = await api.post("contractor-skills/", data);
  return response.data;
};

// Contractor Rating APIs
export const getContractorRatings = async () => {
  const response = await api.get("contractor-ratings/");
  return response.data;
};

export const createContractorRating = async (data) => {
  const response = await api.post("contractor-ratings/", data);
  return response.data;
};

export const verifyContractorRating = async (id) => {
  const response = await api.post(`contractor-ratings/${id}/verify/`);
  return response.data;
};

// Rating Evidence APIs
export const uploadRatingEvidence = async (ratingId, formData) => {
  formData.append("rating", ratingId);
  const response = await api.post("rating-evidence/", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return response.data;
};
