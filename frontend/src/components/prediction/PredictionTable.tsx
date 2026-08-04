"use client";

import { useEffect, useState } from "react";
import { toast } from "sonner";
import {
  deletePrediction,
  getPredictionHistory,
} from "@/services/prediction";

interface Props {
  refresh: boolean;
  refreshTable: () => void;
  setEditingPrediction: (prediction: any) => void;
}

export default function PredictionTable({
  refresh,
  refreshTable,
  setEditingPrediction,
}: Props) {
  const [predictions, setPredictions] = useState<any[]>([]);

  useEffect(() => {
    fetchPredictions();
  }, [refresh]);

  const fetchPredictions = async () => {
    try {
      const data = await getPredictionHistory();
      setPredictions(Array.isArray(data) ? data : []);
    } catch (error) {
      console.error(error);
    }
  };

  const handleDelete = async (id: number) => {
    if (!confirm("Delete this prediction?")) return;

    try {
      await deletePrediction(id);
      toast.success("Prediction deleted successfully");
      refreshTable();
    } catch (error) {
      console.error(error);
      toast.error("Failed to delete prediction");
    }
  };

  return (
    <div className="bg-white rounded-xl shadow-lg p-8">
      <h2 className="text-3xl font-bold text-blue-700 mb-6">
        Prediction History
      </h2>

      <div className="overflow-x-auto">
        <table className="w-full border-collapse">
          <thead className="bg-blue-600 text-white">
            <tr>
              <th className="p-3">Disease</th>
              <th className="p-3">Confidence</th>
              <th className="p-3">Risk Level</th>
              <th className="p-3">Recommendation</th>
              <th className="p-3">Actions</th>
            </tr>
          </thead>

          <tbody>
            {predictions.length === 0 ? (
              <tr>
                <td
                  colSpan={5}
                  className="text-center p-6 text-gray-500"
                >
                  No predictions found.
                </td>
              </tr>
            ) : (
              predictions.map((item) => (
                <tr
                  key={item.id}
                  className="border-b hover:bg-slate-50"
                >
                  <td className="p-3">{item.predicted_disease}</td>

                  <td className="p-3">
                    {item.confidence_score}%
                  </td>

                  <td>
                    <span
                      className={`px-3 py-1 rounded-full text-sm font-semibold ${
                        item.risk_level === "High"
                          ? "bg-red-100 text-red-700"
                          : item.risk_level === "Medium"
                          ? "bg-yellow-100 text-yellow-700"
                          : "bg-green-100 text-green-700"
                      }`}
                    >
                      {item.risk_level}
                    </span>
                  </td>

                  <td className="p-3">
                    {item.recommendation}
                  </td>

                  <td className="p-3 space-x-2">
                    <button
                      onClick={() => setEditingPrediction(item)}
                      className="bg-yellow-500 hover:bg-yellow-600 text-white px-4 py-2 rounded-lg"
                    >
                      Edit
                    </button>

                    <button
                      onClick={() => handleDelete(item.id)}
                      className="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-lg"
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}