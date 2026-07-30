import {
  LayoutDashboard,
  User,
  Stethoscope,
  BrainCircuit,
  FileText,
} from "lucide-react";

export const navigation = [
  {
    name: "Dashboard",
    href: "/dashboard",
    icon: LayoutDashboard,
  },
  {
    name: "Profile",
    href: "/profile",
    icon: User,
  },
  {
    name: "Symptoms",
    href: "/symptoms",
    icon: Stethoscope,
  },
  {
    name: "AI Prediction",
    href: "/prediction",
    icon: BrainCircuit,
  },
  {
    name: "Reports",
    href: "/reports",
    icon: FileText,
  },
];