import api from "./api";

const getToken = () => localStorage.getItem("token");

export const getProfileReport = async () => {
  const response = await api.get("/reports/profile", {
    headers: {
      Authorization: `Bearer ${getToken()}`,
    },
  });

  return response.data;
};

export const getSymptomsReport = async () => {
  const response = await api.get("/reports/symptoms", {
    headers: {
      Authorization: `Bearer ${getToken()}`,
    },
  });

  return response.data;
};

export const getPredictionsReport = async () => {
  const response = await api.get("/reports/predictions", {
    headers: {
      Authorization: `Bearer ${getToken()}`,
    },
  });

  return response.data;
};

export const getSummaryReport = async () => {
  const response = await api.get("/reports/summary", {
    headers: {
      Authorization: `Bearer ${getToken()}`,
    },
  });

  return response.data;
};