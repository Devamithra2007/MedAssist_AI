"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import {
  getDoctorSummary,
  getPatients,
} from "@/services/doctor";

export default function DoctorDashboard() {
    const router = useRouter();
  const [summary, setSummary] = useState<any>(null);
  const [patients, setPatients] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
    

  useEffect(() => {
    loadDashboard();
  }, []);

  const loadDashboard = async () => {
    try {
      const [summaryData, patientData] = await Promise.all([
        getDoctorSummary(),
        getPatients(),
      ]);

      setSummary(summaryData);
      setPatients(patientData);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen text-xl font-bold">
        Loading Doctor Dashboard...
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-100 p-8">

      <h1 className="text-4xl font-bold text-blue-700 mb-8">
        Doctor Dashboard
      </h1>

      {/* Dashboard Cards */}

      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-10">

        <div className="bg-white rounded-xl shadow-lg p-6">
          <h3 className="text-gray-500">Patients</h3>
          <p className="text-4xl font-bold text-blue-600">
            {summary.total_patients}
          </p>
        </div>

        <div className="bg-white rounded-xl shadow-lg p-6">
          <h3 className="text-gray-500">Predictions</h3>
          <p className="text-4xl font-bold text-green-600">
            {summary.total_predictions}
          </p>
        </div>

        <div className="bg-white rounded-xl shadow-lg p-6">
          <h3 className="text-gray-500">Reports</h3>
          <p className="text-4xl font-bold text-purple-600">
            {summary.total_reports}
          </p>
        </div>

        <div className="bg-white rounded-xl shadow-lg p-6">
          <h3 className="text-gray-500">High Risk</h3>
          <p className="text-4xl font-bold text-red-600">
            {summary.high_risk_patients}
          </p>
        </div>

      </div>

      {/* Patient Table */}

      <div className="bg-white rounded-xl shadow-lg p-6">

        <h2 className="text-2xl font-bold mb-6">
          Patients
        </h2>

        <div className="overflow-x-auto">

          <table className="w-full">

            <thead className="bg-blue-600 text-white">

              <tr>
  <th className="p-3 text-left">ID</th>
  <th className="p-3 text-left">Name</th>
  <th className="p-3 text-left">Email</th>
  <th className="p-3 text-left">Role</th>
  <th className="p-3 text-left">Action</th>
</tr>

            </thead>

            <tbody>

              {patients.map((patient) => (

                <tr
                  key={patient.id}
                  className="border-b hover:bg-slate-50"
                >

                  <td className="p-3">{patient.id}</td>

                  <td className="p-3">{patient.full_name}</td>

                  <td className="p-3">{patient.email}</td>

                  <td className="p-3">{patient.role}</td>
                  <td className="p-3">
                    <button
                      onClick={() => router.push(`/doctor/patient/${patient.id}`)}
                      className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
                    >
                      View
                    </button>
                  </td>
                </tr>

              ))}

            </tbody>

          </table>

        </div>

      </div>

    </div>
  );
}