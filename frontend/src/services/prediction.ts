import api from "./api";

export interface PredictionData {
  predicted_disease: string;
  confidence_score: number;
  risk_level: string;
  recommendation: string;
}

export interface AIPredictionRequest {
  symptoms: string[];
}

export interface AIPredictionResponse {
  message: string;
  prediction_id: number;
  disease: string;
  confidence: number;
  risk_level: string;
  recommendation: string;
  created_at: string;
}


// =====================================================
// Manual Prediction
// =====================================================

export const createPrediction = async (
  data: PredictionData
) => {
  const token = localStorage.getItem("token");

  const response = await api.post(
    "/prediction",
    data,
    {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  );

  return response.data;
};


// =====================================================
// AI Disease Prediction
// =====================================================

export const predictDisease = async (
  data: AIPredictionRequest
): Promise<AIPredictionResponse> => {

  const token = localStorage.getItem("token");

  const response = await api.post(
    "/prediction/ai",
    data,
    {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  );

  return response.data;
};


// =====================================================
// Latest Prediction
// =====================================================

export const getLatestPrediction = async () => {

  const token = localStorage.getItem("token");

  const response = await api.get(
    "/prediction",
    {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  );

  return response.data;
};


// =====================================================
// Prediction History
// =====================================================

export const getPredictionHistory = async () => {

  const token = localStorage.getItem("token");

  const response = await api.get(
    "/prediction/history",
    {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  );

  return response.data;
};


// =====================================================
// Update Prediction
// =====================================================

export const updatePrediction = async (
  id: number,
  data: PredictionData
) => {

  const token = localStorage.getItem("token");

  const response = await api.put(
    `/prediction/${id}`,
    data,
    {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  );

  return response.data;
};


// =====================================================
// Delete Prediction
// =====================================================

export const deletePrediction = async (
  id: number
) => {

  const token = localStorage.getItem("token");

  const response = await api.delete(
    `/prediction/${id}`,
    {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  );

  return response.data;
};