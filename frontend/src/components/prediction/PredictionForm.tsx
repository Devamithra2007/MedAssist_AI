"use client";

import { useEffect, useState } from "react";
import { toast } from "sonner";
import {
  createPrediction,
  updatePrediction,
  PredictionData,
} from "@/services/prediction";

interface Props {
  refreshTable: () => void;
  editingPrediction: any;
  setEditingPrediction: (prediction: any) => void;
}

const initialForm: PredictionData = {
  predicted_disease: "",
  confidence_score: 0,
  risk_level: "",
  recommendation: "",
};

export default function PredictionForm({
  refreshTable,
  editingPrediction,
  setEditingPrediction,
}: Props) {
  const [formData, setFormData] = useState<PredictionData>(initialForm);

  useEffect(() => {
    if (editingPrediction) {
      setFormData({
        predicted_disease: editingPrediction.predicted_disease || "",
        confidence_score: editingPrediction.confidence_score || 0,
        risk_level: editingPrediction.risk_level || "",
        recommendation: editingPrediction.recommendation || "",
      });
    } else {
      setFormData(initialForm);
    }
  }, [editingPrediction]);

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    setFormData((prev) => ({
      ...prev,
      [e.target.name]:
        e.target.name === "confidence_score"
          ? Number(e.target.value)
          : e.target.value,
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    try {
      if (editingPrediction) {
        await updatePrediction(editingPrediction.id, formData);
        toast.success("Prediction updated successfully");
      } else {
        await createPrediction(formData);
        toast.success("Prediction created successfully");
      }

      setFormData(initialForm);
      setEditingPrediction(null);
      refreshTable();
    } catch (error) {
      console.error(error);
      toast.error("Operation failed");
    }
  };

  return (
    <div className="bg-white rounded-xl shadow-lg p-8">
      <h2 className="text-3xl font-bold text-blue-700 mb-6">
        {editingPrediction ? "Update Prediction" : "Create Prediction"}
      </h2>

      <form
        onSubmit={handleSubmit}
        className="grid grid-cols-1 gap-5"
      >
        <input
          name="predicted_disease"
          placeholder="Predicted Disease"
          value={formData.predicted_disease}
          onChange={handleChange}
          className="border rounded-lg p-3"
        />

        <input
          type="number"
          name="confidence_score"
          placeholder="Confidence Score"
          value={formData.confidence_score}
          onChange={handleChange}
          className="border rounded-lg p-3"
        />

        <input
          name="risk_level"
          placeholder="Risk Level"
          value={formData.risk_level}
          onChange={handleChange}
          className="border rounded-lg p-3"
        />

        <textarea
          name="recommendation"
          placeholder="Recommendation"
          value={formData.recommendation}
          onChange={handleChange}
          className="border rounded-lg p-3"
          rows={4}
        />

        <div className="flex gap-4">
          <button
            type="submit"
            className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg"
          >
            {editingPrediction ? "Update Prediction" : "Save Prediction"}
          </button>

          {editingPrediction && (
            <button
              type="button"
              onClick={() => {
                setEditingPrediction(null);
                setFormData(initialForm);
              }}
              className="bg-gray-500 hover:bg-gray-600 text-white px-6 py-3 rounded-lg"
            >
              Cancel
            </button>
          )}
        </div>
      </form>
    </div>
  );
}