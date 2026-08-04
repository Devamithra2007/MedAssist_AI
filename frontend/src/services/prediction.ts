import api from "./api";

export interface PredictionData {
  predicted_disease: string;
  confidence_score: number;
  risk_level: string;
  recommendation: string;
}

export const createPrediction = async (data: PredictionData) => {
  const token = localStorage.getItem("token");

  const response = await api.post("/prediction", data, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  return response.data;
};

export const getLatestPrediction = async () => {
  const token = localStorage.getItem("token");

  const response = await api.get("/prediction", {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  return response.data;
};

export const getPredictionHistory = async () => {
  const token = localStorage.getItem("token");

  const response = await api.get("/prediction/history", {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  return response.data;
};

export const updatePrediction = async (
  id: number,
  data: PredictionData
) => {
  const token = localStorage.getItem("token");

  const response = await api.put(`/prediction/${id}`, data, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  return response.data;
};

export const deletePrediction = async (id: number) => {
  const token = localStorage.getItem("token");

  const response = await api.delete(`/prediction/${id}`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  return response.data;
};