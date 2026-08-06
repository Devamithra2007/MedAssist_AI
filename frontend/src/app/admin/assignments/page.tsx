"use client";

import { useEffect, useState } from "react";

import DashboardLayout from "@/components/layouts/DashboardLayout";
import WelcomeBanner from "@/components/dashboard/welcomeBanner";

import AssignmentForm from "@/components/assignment/AssignmentForm";
import AssignmentTable from "@/components/assignment/AssignmentTable";

import {
  getDoctors,
  getPatients,
  getAssignments,
} from "@/services/assignment";

export default function AssignmentPage() {
  const [doctors, setDoctors] = useState([]);
  const [patients, setPatients] = useState([]);
  const [assignments, setAssignments] = useState([]);

  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const doctorData = await getDoctors();
      const patientData = await getPatients();
      const assignmentData = await getAssignments();

      setDoctors(doctorData);
      setPatients(patientData);
      setAssignments(assignmentData);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <DashboardLayout>
        <div className="flex h-full items-center justify-center text-xl">
          Loading...
        </div>
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout>
      <WelcomeBanner
        name="Administrator"
        role="Admin"
        message="Assign patients to doctors and manage assignments."
      />

      <div className="mt-8 space-y-8">

        <AssignmentForm
          doctors={doctors}
          patients={patients}
          onSuccess={loadData}
        />

        <AssignmentTable
          assignments={assignments}
          onRefresh={loadData}
        />

      </div>
    </DashboardLayout>
  );
}