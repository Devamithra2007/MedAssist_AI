import {
  Stethoscope,
  FileText,
  User,
} from "lucide-react";

const actions = [
  {
    title: "Analyze Symptoms",
    icon: Stethoscope,
  },
  {
    title: "View Reports",
    icon: FileText,
  },
  {
    title: "Update Profile",
    icon: User,
  },
];

export default function QuickActions() {
  return (
    <div className="rounded-2xl bg-white p-6 shadow-md">
      <h2 className="mb-6 text-xl font-bold">
        Quick Actions
      </h2>

      <div className="grid grid-cols-1 gap-4 md:grid-cols-3">
        {actions.map((action) => {
          const Icon = action.icon;

          return (
            <button
              key={action.title}
              className="rounded-xl border p-6 hover:bg-sky-50 transition"
            >
              <Icon
                size={32}
                className="mx-auto mb-3 text-sky-700"
              />

              <p>{action.title}</p>
            </button>
          );
        })}
      </div>
    </div>
  );
}