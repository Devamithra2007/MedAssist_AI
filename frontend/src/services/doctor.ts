import api from "./api";

const token = () => localStorage.getItem("token");

export const getDoctorSummary = async () => {
  const res = await api.get("/doctor/summary", {
    headers: {
      Authorization: `Bearer ${token()}`,
    },
  });

  return res.data;
};

export const getPatients = async () => {
  const res = await api.get("/doctor/patients", {
    headers: {
      Authorization: `Bearer ${token()}`,
    },
  });

  return res.data;
};

export const getPatientProfile = async (id: number) => {
  console.log("TOKEN:", token());

  const res = await api.get(`/doctor/patient/${id}`, {
    headers: {
      Authorization: `Bearer ${token()}`,
    },
  });

  return res.data;
};

export const getPatientSymptoms = async (id: number) => {
  const res = await api.get(`/doctor/patient/${id}/symptoms`, {
    headers: {
      Authorization: `Bearer ${token()}`,
    },
  });

  return res.data;
};

export const getPatientPredictions = async (id: number) => {
  const res = await api.get(`/doctor/patient/${id}/predictions`, {
    headers: {
      Authorization: `Bearer ${token()}`,
    },
  });

  return res.data;
};

