import DashboardLayout from "@/components/layout/DashboardLayout";
import StatCard from "@/components/dashboard/StatCard";
import QuickActions from "@/components/dashboard/QuickActions";
import RecentActivity from "@/components/dashboard/RecentActivity";

import {
  HeartPulse,
  BrainCircuit,
  FileText,
  User,
} from "lucide-react";

export default function DashboardPage() {
  return (
    <DashboardLayout>
      <div className="space-y-8">

        {/* Welcome Section */}
        <section>
          <h1 className="text-4xl font-bold text-gray-800">
            👋 Welcome to MedAssist AI
          </h1>

          <p className="mt-2 text-gray-500">
            Your AI-powered healthcare companion.
          </p>
        </section>

        {/* Statistics */}
        <section className="grid grid-cols-1 gap-6 md:grid-cols-2 xl:grid-cols-4 text-gray-800">

          <StatCard
            title="Health Score"
            value="98%"
            icon={HeartPulse}
            color="bg-red-500"

          />

          <StatCard
            title="AI Predictions"
            value="12"
            icon={BrainCircuit}
            color="bg-blue-600"
          />

          <StatCard
            title="Reports"
            value="5"
            icon={FileText}
            color="bg-green-600"
          />

          <StatCard
            title="Profile"
            value="80%"
            icon={User}
            color="bg-purple-600"
          />

        </section>

        {/* Quick Actions */}
        <QuickActions />

        {/* Recent Activity */}
        <RecentActivity />

      </div>
    </DashboardLayout>
  );
}